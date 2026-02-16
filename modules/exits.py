import streamlit as st
from modules import db
import datetime

def show_exit_management(user_id, is_admin=False):
    if is_admin:
        show_admin_exits()
    else:
        show_employee_resignation(user_id)

def show_admin_exits():
    st.markdown("## 🚪 Exit & Separation Management")
    
    # List Pending Resignations
    st.markdown("### ⏳ Pending Resignations")
    query = """
    SELECT s.employee_id, e.name, s.resignation_date, s.last_working_day, s.reason, s.status, s.exit_interview_notes
    FROM separations s
    JOIN employees e ON s.employee_id = e.id
    WHERE s.status = 'Pending'
    """
    df = db.run_query(query)
    
    if df.empty:
        st.info("No pending resignations.")
    else:
        for _, row in df.iterrows():
            with st.expander(f"{row['name']} (Resigned: {row['resignation_date']})"):
                st.write(f"**Reason:** {row['reason']}")
                st.write(f"**Proposed LWD:** {row['last_working_day']}")
                
                notes = st.text_area("Exit Interview Notes", key=f"notes_{row['employee_id']}")
                
                c1, c2 = st.columns(2)
                if c1.button("✅ Accept & Process F&F", key=f"acc_{row['employee_id']}"):
                    ops = [
                        ("UPDATE separations SET status='Processed', exit_interview_notes=? WHERE employee_id=?", (notes, row['employee_id'])),
                        ("UPDATE employees SET status='Resigned' WHERE id=?", (row['employee_id'],))
                    ]
                    if db.execute_transaction(ops):
                        st.success("Resignation Processed. Employee marked as 'Resigned'.")
                        st.rerun()
                        
                if c2.button("❌ Reject / Discuss", key=f"rej_{row['employee_id']}"):
                     st.warning("Action: Schedule a retention meeting.")

def show_employee_resignation(emp_id):
    st.markdown("## 🚪 Resignation Portal")
    
    # Check current status
    curr = db.run_query("SELECT status, last_working_day FROM separations WHERE employee_id=?", (emp_id,))
    
    if not curr.empty:
        st.warning(f"⚠️ You have already submitted a resignation. Status: **{curr.iloc[0]['status']}**")
        st.info(f"Last Working Day: {curr.iloc[0]['last_working_day']}")
        return
        
    st.write("We are sorry to see you go. Please fill out the details below.")
    
    with st.form("resign_form"):
        lwd = st.date_input("Proposed Last Working Day", min_value=datetime.date.today())
        reason = st.text_area("Reason for Leaving")
        
        submitted = st.form_submit_button("Submit Resignation")
        
        if submitted:
            query = "INSERT INTO separations (employee_id, resignation_date, last_working_day, reason) VALUES (?, ?, ?, ?)"
            if db.execute_transaction([(query, (emp_id, datetime.date.today(), lwd, reason))]):
                st.success("Resignation submitted to HR.")
                st.rerun()
