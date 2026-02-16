import streamlit as st
import pandas as pd
from modules import core, analytics, performance, recruitment, engagement, onboarding, archival, db, auth, ess, payroll, assets, docs, approvals, exits

# -----------------------------------------------------------------------------
# Page Config
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Zentara | Intelligent HRMS",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded"
)

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

local_css("assets/custom.css")

# -----------------------------------------------------------------------------
# Authentication
# -----------------------------------------------------------------------------
if 'role' not in st.session_state:
    st.session_state['role'] = None

if st.session_state['role'] is None:
    auth.login_page()
    st.stop()

# -----------------------------------------------------------------------------
# ROUTING
# -----------------------------------------------------------------------------
role = st.session_state['role']
auth.logout()

if role == "employee":
    # -------------------------------------------------------------------------
    # EMPLOYEE VIEW
    # -------------------------------------------------------------------------
    st.sidebar.title("🧘 Zentara")
    st.sidebar.markdown("### Employee Portal")
    
    page = st.sidebar.radio("Navigate", [
        "My Profile", 
        "My Attendance", 
        "My Payslips", 
        "Leave Application",
        "Resignation / Limit"
    ])
    
    if page == "My Profile":
        ess.show_my_profile(st.session_state['user_id'])
    elif page == "My Attendance":
        ess.show_my_attendance(st.session_state['user_id'])
    elif page == "My Payslips":
        payroll.show_employee_payslips(st.session_state['user_id'])
    elif page == "Leave Application":
        ess.show_leave_application(st.session_state['user_id'])
    elif page == "Resignation / Limit":
        exits.show_employee_resignation(st.session_state['user_id'])

elif role == "admin":
    # -------------------------------------------------------------------------
    # ADMIN VIEW
    # -------------------------------------------------------------------------
    st.sidebar.title("🧘 Zentara")
    st.sidebar.markdown("### Admin Control Center")

    page = st.sidebar.radio("Navigate", [
        "🏠 Dashboard",
        "✅ Approvals",
        "💰 Payroll Engine",
        "✍️ Onboarding",
        "📂 Workforce Directory",
        "💻 Assets",
        "📄 Documents",
        "🚪 Exits",
        "🔥 Attrition Risk",
        "⭐ Performance",
        "🧊 Glacier Services"
    ])
    
    # Load Data
    df_analytics = core.load_data()

    if page == "🏠 Dashboard":
        st.title("Executive Workforce Dashboard")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Headcount", len(df_analytics))
        m2.metric("Payroll Cost (Est)", f"₹ {df_analytics['Salary'].sum()/10000000:.2f} Cr")
        m3.metric("Pending Leaves", "Check Approvals") 
        m4.metric("Assets Assigned", "124")

    elif page == "✅ Approvals":
        approvals.show_approval_dashboard("ADMIN", is_admin=True)

    elif page == "💰 Payroll Engine":
        payroll.show_admin_payroll()

    elif page == "✍️ Onboarding":
        onboarding.show_onboarding_form()

    elif page == "📂 Workforce Directory":
        onboarding.show_employee_directory()
        
    elif page == "💻 Assets":
        assets.show_asset_registry()
        
    elif page == "📄 Documents":
        docs.show_doc_manager()

    elif page == "🚪 Exits":
        exits.show_admin_exits()

    elif page == "🔥 Attrition Risk":
        analytics.show_attrition_dashboard(df_analytics)

    elif page == "⭐ Performance":
        performance.show_performance_dashboard(df_analytics)

    elif page == "🧊 Glacier Services":
        st.title("🧊 Glacier Archival")
        if st.button("Archive Data"):
            archival.archive_data()
            st.success("Archived!")
