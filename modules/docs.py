import streamlit as st
from modules import db

def show_doc_manager():
    st.markdown("## 📄 Document Manager")
    st.info("Central Repository for Employee Documents (Offer Letters, IDs, etc.)")
    
    # Upload (Mock)
    st.file_uploader("Upload Document", type=['pdf', 'jpg', 'png'])
    st.caption("File storage is simulated in this demo.")
    
    # List (Mock)
    st.markdown("### Recent Uploads")
    st.write("No documents found.")
