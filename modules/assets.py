import streamlit as st
from modules import db
import datetime

def show_asset_registry():
    st.markdown("## 💻 IT Asset Registry")
    
    # Add Asset
    with st.expander("➕ Add New Asset"):
        with st.form("add_asset"):
            c1, c2 = st.columns(2)
            a_type = c1.selectbox("Type", ["Laptop", "Monitor", "Keyboard", "Mouse", "Phone"])
            model = c2.text_input("Model Name")
            serial = st.text_input("Serial Number")
            status = st.selectbox("Status", ["In Stock", "Assigned", "Repair", "Scrapped"])
            
            submitted = st.form_submit_button("Add Asset")
            if submitted:
                # Basic Insert
                query = "INSERT INTO assets (asset_type, serial_number, model_name, status) VALUES (?, ?, ?, ?)"
                if db.execute_transaction([(query, (a_type, serial, model, status))]):
                    st.success(f"Asset {serial} Added to Zentara Registry!")
                    st.rerun()

    # View Assets
    st.markdown("### Asset Inventory")
    df = db.run_query("SELECT * FROM assets")
    st.dataframe(df, use_container_width=True)
