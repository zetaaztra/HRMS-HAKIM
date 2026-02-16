import pandas as pd
import datetime
import os
import streamlit as st
from modules import db

BACKUP_DIR = "backups/glacier"

def ensure_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def archive_data():
    ensure_backup_dir()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    tables = ["employees", "compliance", "banking", "addresses"]
    
    archived_files = []
    
    conn = db.get_connection()
    try:
        for table in tables:
            df = pd.read_sql(f"SELECT * FROM {table}", conn)
            if not df.empty:
                filename = f"{BACKUP_DIR}/{table}_{timestamp}.csv"
                df.to_csv(filename, index=False)
                archived_files.append(filename)
        return archived_files
    except Exception as e:
        st.error(f"Archival failed: {e}")
        return []
    finally:
        conn.close()

def list_archives():
    ensure_backup_dir()
    files = os.listdir(BACKUP_DIR)
    return sorted(files, reverse=True)
