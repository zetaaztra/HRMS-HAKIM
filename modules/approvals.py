import streamlit as st
from modules import db
import datetime

def show_approval_dashboard(user_id, is_admin=False):
    st.markdown("## ✅ Approval Dashboard")
    
    # 1. Fetch Pending Requests
    # If Admin -> Show All Pending
    # If Manager -> Show Pending where employees.manager_id = user_id
    
    if is_admin:
        query = """
        SELECT r.id, r.employee_id, e.name, r.leave_type, r.start_date, r.end_date, r.reason, r.status 
        FROM leave_requests r
        JOIN employees e ON r.employee_id = e.id
        WHERE r.status = 'Pending'
        ORDER BY r.start_date ASC
        """
        params = ()
    else:
        query = """
        SELECT r.id, r.employee_id, e.name, r.leave_type, r.start_date, r.end_date, r.reason, r.status 
        FROM leave_requests r
        JOIN employees e ON r.employee_id = e.id
        WHERE r.status = 'Pending' AND e.manager_id = ?
        ORDER BY r.start_date ASC
        """
        params = (user_id,)
        
    df = db.run_query(query, params)
    
    if df.empty:
        st.info("🎉 No pending approvals! You are all caught up.")
        return
        
    st.markdown(f"### ⏳ Pending Requests ({len(df)})")
    
    for _, row in df.iterrows():
        with st.expander(f"{row['name']} - {row['leave_type']} ({row['start_date']} to {row['end_date']})"):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(f"**Reason:** {row['reason']}")
                st.caption(f"Employee ID: {row['employee_id']}")
                
            with c2:
                # Approve
                if st.button("✅ Approve", key=f"app_{row['id']}"):
                    update_status(row['id'], 'Approved', user_id)
                    st.rerun()
                    
                # Reject
                if st.button("❌ Reject", key=f"rej_{row['id']}"):
                    update_status(row['id'], 'Rejected', user_id)
                    st.rerun()

def update_status(req_id, status, approver_id):
    query = """
    UPDATE leave_requests 
    SET status = ?, approved_by = ?, approval_date = ? 
    WHERE id = ?
    """
    if db.execute_transaction([(query, (status, approver_id, datetime.date.today(), req_id))]):
        st.toast(f"Request {status} Successfully!", icon="🚀")
