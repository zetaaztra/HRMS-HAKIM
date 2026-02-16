import streamlit as st
import datetime
import uuid
from modules import db

def show_onboarding_form():
    st.markdown("## ✍️ New Employee Onboarding")
    st.info("Complete all statutory and personal details for the new joinee.")
    
    # Initialize session state for form data if not exists (optional, Streamlit handles widgets)
    
    with st.form("onboarding_form", clear_on_submit=True):
        
        # --- TAB 1: Personal Details ---
        st.subheader("1. Personal Information")
        c1, c2, c3 = st.columns(3)
        with c1:
            first_name = st.text_input("First Name")
        with c2:
            last_name = st.text_input("Last Name")
        with c3:
            dob = st.date_input("Date of Birth", min_value=datetime.date(1960, 1, 1))
            
        c4, c5, c6 = st.columns(3)
        with c4:
            mobile = st.text_input("Mobile Number", placeholder="+91 XXXXX XXXXX")
        with c5:
            email = st.text_input("Personal Email")
        with c6:
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            
        st.markdown("---")
        
        # --- TAB 2: Address Details ---
        st.subheader("2. Address Details")
        current_addr = st.text_area("Current Address", height=100)
        perm_addr = st.text_area("Permanent Address (Same as Current?)", height=100)
        
        a1, a2, a3 = st.columns(3)
        with a1:
            city = st.text_input("City")
        with a2:
            state = st.selectbox("State", ["Karnataka", "Maharashtra", "Delhi", "Tamil Nadu", "Telangana", "Other"])
        with a3:
            pincode = st.text_input("Pincode")

        st.markdown("---")

        # --- TAB 3: Professional Details ---
        st.subheader("3. Professional Details")
        p1, p2, p3 = st.columns(3)
        with p1:
            emp_id = st.text_input("Employee ID (Auto-generated if empty)", value=str(uuid.uuid4())[:8], disabled=True)
        with p2:
            dept = st.selectbox("Department", ["Engineering", "Sales", "Marketing", "HR", "Finance"])
        with p3:
            role = st.text_input("Designation / Role")
            
        p4, p5 = st.columns(2)
        with p4:
            joining_date = st.date_input("Date of Joining", value=datetime.date.today())
        with p5:
            manager_id = st.text_input("Reporting Manager ID")

        st.markdown("---")

        # --- TAB 4: Statutory Compliance (Indian) ---
        st.subheader("4. Statutory & Compliance")
        s1, s2 = st.columns(2)
        with s1:
            pan = st.text_input("PAN Number", max_chars=10, help="Format: ABCDE1234F")
        with s2:
            aadhar = st.text_input("Aadhar Number", max_chars=12)
            
        s3, s4 = st.columns(2)
        with s3:
            uan = st.text_input("UAN (PF Layout)", help="Universal Account Number")
        with s4:
            esi = st.text_input("ESI Number")

        st.markdown("---")

        # --- TAB 5: Banking ---
        st.subheader("5. Banking Details")
        b1, b2, b3 = st.columns(3)
        with b1:
            bank_name = st.text_input("Bank Name")
        with b2:
            account_no = st.text_input("Account Number")
        with b3:
            ifsc = st.text_input("IFSC Code")

        submitted = st.form_submit_button("Submit & Onboard Employee", type="primary")
        
        if submitted:
            # Validate basic fields
            if not first_name or not pan or not aadhar:
                st.error("❌ Mandatory fields missing: Name, PAN, or Aadhar.")
            else:
                full_name = f"{first_name} {last_name}"
                
                # Transactional Insert
                ops = []
                
                # 1. Employee
                ops.append((
                    "INSERT INTO employees (id, name, department, role, joining_date, email, mobile, blood_group, dob) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (emp_id, full_name, dept, role, joining_date, email, mobile, blood_group, dob)
                ))
                
                # 2. Compliance
                ops.append((
                    "INSERT INTO compliance (employee_id, pan_number, aadhar_number, uan_number, esi_number) VALUES (?, ?, ?, ?, ?)",
                    (emp_id, pan, aadhar, uan, esi)
                ))
                
                # 3. Banking
                ops.append((
                    "INSERT INTO banking (employee_id, bank_name, account_number, ifsc_code) VALUES (?, ?, ?, ?)",
                    (emp_id, bank_name, account_no, ifsc)
                ))
                
                # 4. Address
                ops.append((
                    "INSERT INTO addresses (employee_id, current_address, permanent_address, city, state, pincode) VALUES (?, ?, ?, ?, ?, ?)",
                    (emp_id, current_addr, full_name, city, state, pincode) # Using full_name as placeholder if perm addr empty logic needed
                ))

                if db.execute_transaction(ops):
                    st.success(f"✅ Employee {full_name} ({emp_id}) onboarded successfully!")
                    st.balloons()
                else:
                    st.error("❌ Failed to save record. Database transaction rolled back.")

def show_employee_directory():
    st.markdown("## 📂 Employee Directory (SQL Live)")
    
    # Join queries to show rich data
    query = """
    SELECT 
        e.id, e.name, e.department, e.role, 
        c.pan_number, c.aadhar_number, 
        b.bank_name
    FROM employees e
    LEFT JOIN compliance c ON e.id = c.employee_id
    LEFT JOIN banking b ON e.id = b.employee_id
    """
    
    df = db.run_query(query)
    st.dataframe(df, use_container_width=True)
