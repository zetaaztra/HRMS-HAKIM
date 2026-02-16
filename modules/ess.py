import streamlit as st
from modules import db
import pandas as pd
import datetime

def show_employee_portal():
    emp_id = st.session_state.get('user_id')
    if not emp_id:
        st.error("Session Error. Please re-login.")
        return

    # Fetch User Name for Welcome Message
    user_df = db.run_query("SELECT name FROM employees WHERE id = ?", (emp_id,))
    emp_name = user_df.iloc[0]['name'] if not user_df.empty else "Employee"
    
    st.title(f"👋 Welcome, {emp_name}")
    
    tab1, tab2, tab3 = st.tabs(["👤 My Profile", "📅 Attendance", "📝 Leave Application"])
    
    with tab1:
        show_my_profile(emp_id)
        
    with tab2:
        show_my_attendance(emp_id)
        
    with tab3:
        show_leave_application(emp_id)

def show_my_profile(emp_id):
    st.subheader("My Digital Profile")
    
    # 1. Fetch Full Data
    query = """
    SELECT 
        e.*, c.pan_number, c.aadhar_number, c.uan_number, c.esi_number,
        b.bank_name, b.account_number, b.ifsc_code,
        a.current_address, a.permanent_address
    FROM employees e
    LEFT JOIN compliance c ON e.id = c.employee_id
    LEFT JOIN banking b ON e.id = b.employee_id
    LEFT JOIN addresses a ON e.id = a.employee_id
    WHERE e.id = ?
    """
    df = db.run_query(query, (emp_id,))
    
    if df.empty:
        st.warning("Profile not found.")
        return
        
    rec = df.iloc[0]
    
    # Display in Sections
    p1, p2 = st.columns(2)
    with p1:
        st.info("Personal Details")
        st.write(f"**Name:** {rec['name']}")
        st.write(f"**Role:** {rec['role']}")
        st.write(f"**Dept:** {rec['department']}")
        st.write(f"**Mobile:** {rec['mobile']}")
        st.write(f"**Email:** {rec['email']}")
        
    with p2:
        st.info("Statutory Data (Verified)")
        st.write(f"**PAN:** {rec['pan_number']}")
        st.write(f"**Aadhar:** {rec['aadhar_number']}")
        st.write(f"**UAN:** {rec['uan_number']}")
        st.write(f"**ESI:** {rec['esi_number']}")
        
    st.markdown("---")
    b1, b2 = st.columns(2)
    with b1:
        st.warning("Bank Details (Salary Account)")
        st.write(f"**Bank:** {rec['bank_name']}")
        st.write(f"**Account:** {rec['account_number']}")
        st.write(f"**IFSC:** {rec['ifsc_code']}")
        
    with b2:
        st.success("Address")
        st.write(f"**Current:** {rec['current_address']}")
        st.write(f"**Permanent:** {rec['permanent_address']}")

def show_my_attendance(emp_id):
    st.subheader("Attendance History")
    
    query = "SELECT date, status, check_in, check_out, hours_worked FROM attendance WHERE employee_id = ? ORDER BY date DESC"
    df = db.run_query(query, (emp_id,))
    
    if df.empty:
        st.info("No attendance records found yet.")
    else:
        # Metrics
        present_days = len(df[df['status'] == 'Present'])
        absent_days = len(df[df['status'] == 'Absent'])
        st.metric("Total Present Days (This Month)", present_days)
        
        st.dataframe(df, use_container_width=True)

def show_leave_application(emp_id):
    st.subheader("Apply for Leave")
    
    # History
    st.markdown("#### recent Requests")
    hist = db.run_query("SELECT start_date, end_date, leave_type, status FROM leave_requests WHERE employee_id = ? ORDER BY id DESC LIMIT 5", (emp_id,))
    st.table(hist)
    
    # Form
    with st.form("leave_form"):
        l_type = st.selectbox("Leave Type", ["Casual Leave (CL)", "Sick Leave (SL)", "Privilege Leave (PL)"])
        d1, d2 = st.columns(2)
        start_date = d1.date_input("Start Date")
        end_date = d2.date_input("End Date")
        reason = st.text_area("Reason")
        
        submitted = st.form_submit_button("Submit Request")
        
        if submitted:
            query = "INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, reason) VALUES (?, ?, ?, ?, ?)"
            if db.execute_transaction([(query, (emp_id, l_type, start_date, end_date, reason))]):
                st.success("Leave request submitted successfully!")
                st.rerun()
