import streamlit as st
import pandas as pd
import datetime
from modules import db

def calculate_salary_components(annual_ctc):
    """
    Standard Indian Salary Structure:
    - Basic: 50% of CTC
    - HRA: 50% of Basic
    - Special: Balancing Figure
    - PF: 12% of Basic (Max 1800 usually, but simplified here)
    - PT: Flat 200 (Karnataka approx)
    - TDS: Simplified 10% on Taxable > 5L
    """
    monthly_ctc = annual_ctc / 12
    
    basic = monthly_ctc * 0.5
    hra = basic * 0.5
    
    # PF (Employer + Employee contribution usually, keeping simple for Net calc)
    # Employee Share usually 12% of Basic
    pf = min(basic * 0.12, 1800) if basic > 15000 else basic * 0.12
    
    pt = 200 # Standard flat rate
    
    # Simple TDS: If Annual > 5L, 10% of monthly (Very rough approx)
    tds = (monthly_ctc * 0.1) if annual_ctc > 500000 else 0
    
    total_deductions = pf + pt + tds
    
    # Special Allowance is the remainder to match Gross (ignoring employer PF part for simplicity)
    # Gross = Basic + HRA + Special
    # We want Gross approx equal to Monthly CTC for this simple model
    special = monthly_ctc - (basic + hra)
    if special < 0: special = 0
    
    net_salary = basic + hra + special - total_deductions
    
    return {
        "Basic Salary": round(basic, 2),
        "HRA": round(hra, 2),
        "Special Allowance": round(special, 2),
        "PF Deduction": round(pf, 2),
        "Professional Tax": round(pt, 2),
        "TDS": round(tds, 2),
        "Net Salary": round(net_salary, 2),
        "Gross Earnings": round(basic + hra + special, 2),
        "Total Deductions": round(total_deductions, 2)
    }

def run_payroll_batch(month, year):
    """Generates payslips for all active employees for the given month."""
    
    # Get all active employees with salary
    query = "SELECT id, salary FROM employees WHERE status = 'Active'"
    employees = db.run_query(query)
    
    generated_count = 0
    total_payout = 0
    
    ops = []
    
    for _, emp in employees.iterrows():
        ctc = emp['salary']
        if not ctc or ctc == 0: continue
        
        comps = calculate_salary_components(ctc)
        
        # Check if already generated
        check = db.run_query("SELECT id FROM payslips WHERE employee_id=? AND month=? AND year=?", 
                             (emp['id'], month, year))
        if not check.empty:
            continue
            
        ops.append((
            """INSERT INTO payslips (
                employee_id, month, year, basic_salary, hra, special_allowance, 
                pf_deduction, pt_deduction, tds_deduction, net_salary, generated_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (emp['id'], month, year, comps['Basic Salary'], comps['HRA'], comps['Special Allowance'],
             comps['PF Deduction'], comps['Professional Tax'], comps['TDS'], comps['Net Salary'],
             datetime.date.today())
        ))
        
        generated_count += 1
        total_payout += comps['Net Salary']
        
    if ops:
        if db.execute_transaction(ops):
            return generated_count, total_payout
    return 0, 0

def show_admin_payroll():
    st.markdown("## 💰 Payroll Processing Center")
    
    # 1. Run Payroll
    with st.expander("🚀 Run Payroll Batch", expanded=True):
        c1, c2 = st.columns(2)
        month = c1.selectbox("Month", ["January", "February", "March", "April", "May", "June", 
                                     "July", "August", "September", "October", "November", "December"])
        year = c2.number_input("Year", min_value=2023, value=datetime.date.today().year)
        
        if st.button("Run Payroll Process"):
            with st.spinner("Calculating Taxes & Salaries..."):
                count, payout = run_payroll_batch(month, year)
                if count > 0:
                    st.success(f"✅ Successfully generated {count} payslips!")
                    st.metric("Total Payout", f"₹ {payout:,.2f}")
                else:
                    st.warning("No new payslips generated (Already exist or no active employees).")

    # 2. View History
    st.markdown("### Payroll History")
    history = db.run_query("""
        SELECT p.id, e.name, p.month, p.year, p.net_salary, p.status 
        FROM payslips p 
        JOIN employees e ON p.employee_id = e.id 
        ORDER BY p.id DESC LIMIT 50
    """)
    st.dataframe(history, use_container_width=True)

def show_employee_payslips(emp_id):
    st.markdown("## 📄 My Payslips")
    
    slips = db.run_query("SELECT * FROM payslips WHERE employee_id = ? ORDER BY id DESC", (emp_id,))
    
    if slips.empty:
        st.info("No payslips available yet.")
        return
        
    for _, slip in slips.iterrows():
        with st.expander(f"{slip['month']} {slip['year']} - ₹{slip['net_salary']:,.0f}"):
            # Payslip UI
            st.markdown(f"### Payslip for {slip['month']} {slip['year']}")
            
            c1, c2 = st.columns(2)
            c1.write("**Earnings**")
            c1.write(f"Basic: ₹{slip['basic_salary']:,.2f}")
            c1.write(f"HRA: ₹{slip['hra']:,.2f}")
            c1.write(f"Special: ₹{slip['special_allowance']:,.2f}")
            c1.markdown(f"**Gross: ₹{slip['basic_salary']+slip['hra']+slip['special_allowance']:,.2f}**")
            
            c2.write("**Deductions**")
            c2.write(f"PF: ₹{slip['pf_deduction']:,.2f}")
            c2.write(f"PT: ₹{slip['pt_deduction']:,.2f}")
            c2.write(f"TDS: ₹{slip['tds_deduction']:,.2f}")
            c2.markdown(f"**Total Ded: ₹{slip['pf_deduction']+slip['pt_deduction']+slip['tds_deduction']:,.2f}**")
            
            st.markdown("---")
            st.markdown(f"<h3 style='text-align: right;'>Net Pay: ₹{slip['net_salary']:,.2f}</h3>", unsafe_allow_html=True)
            st.button("Download PDF (Mock)", key=f"dl_{slip['id']}")
