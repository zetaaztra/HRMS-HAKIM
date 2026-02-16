import streamlit as st
from modules import db

def check_password(username, password):
    """Returns 'admin', 'employee' (with ID), or None."""
    
    # 1. Admin Login
    if username == "admin" and password == "admin":
        return "admin", "SUPERUSER"
    
    # 2. Employee Login (Check DB)
    # Generic password 'password' for demo, or match ID-ID for simplicity
    # In real world: verify hash
    query = "SELECT id, name FROM employees WHERE id = ?"
    df = db.run_query(query, (username,))
    
    if not df.empty:
        if password == "password": # Hardcoded for demo
            return "employee", df.iloc[0]['id']
            
    return None, None

def login_page():
    st.markdown("<h1 style='text-align: center; color: #00C9FF;'>Zentara Login</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Intelligent HR & Workforce Harmony Platform</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("User ID / Admin ID", placeholder="admin or EMP-XXXX")
            password = st.text_input("Password", type="password", placeholder="admin or password")
            submitted = st.form_submit_button("Login", type="primary")
            
            if submitted:
                role, emp_id = check_password(username, password)
                if role:
                    st.session_state['role'] = role
                    st.session_state['user_id'] = emp_id
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
                    
            st.markdown("---")
            with st.expander("🔑 Forgot Password?"):
                st.markdown("""
                **Employees:** Contact HR Admin to reset your password.
                
                **Admins:** Use the recovery key in `config.yaml` or contact system support.
                """)
            
            with st.expander("ℹ️ Demo Credentials"):
                st.info("""
                **Admin:** admin / admin
                
                **Employee:** EMP001 / password
                """)
                
    st.markdown("""
        <div style='text-align: center; margin-top: 50px; color: #666;'>
            <p>Product of <b>Hakim Sulthan Technologies</b></p>
        </div>
    """, unsafe_allow_html=True)

def logout():
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()
