import sqlite3
import pandas as pd
import streamlit as st
import datetime

DB_FILE = "hrms.db"

def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # 1. Employees Table (Core)
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
        id TEXT PRIMARY KEY,
        name TEXT,
        department TEXT,
        role TEXT,
        joining_date DATE,
        status TEXT DEFAULT 'Active',
        manager_id TEXT,
        email TEXT,
        mobile TEXT,
        blood_group TEXT,
        dob DATE,
        salary REAL
    )''')
    
    # 2. Compliance Table (Indian Context)
    c.execute('''CREATE TABLE IF NOT EXISTS compliance (
        employee_id TEXT PRIMARY KEY,
        pan_number TEXT,
        aadhar_number TEXT,
        uan_number TEXT,
        esi_number TEXT,
        pf_number TEXT,
        FOREIGN KEY(employee_id) REFERENCES employees(id)
    )''')
    
    # 3. Banking Table
    c.execute('''CREATE TABLE IF NOT EXISTS banking (
        employee_id TEXT PRIMARY KEY,
        bank_name TEXT,
        account_number TEXT,
        ifsc_code TEXT,
        branch_name TEXT,
        FOREIGN KEY(employee_id) REFERENCES employees(id)
    )''')

    # 4. Address Table
    c.execute('''CREATE TABLE IF NOT EXISTS addresses (
        employee_id TEXT PRIMARY KEY,
        current_address TEXT,
        permanent_address TEXT,
        city TEXT,
        state TEXT,
        pincode TEXT,
        FOREIGN KEY(employee_id) REFERENCES employees(id)
    )''')

    # 5. Attendance Table
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        date DATE,
        status TEXT,
        check_in TIME,
        check_out TIME,
        hours_worked REAL,
        FOREIGN KEY(employee_id) REFERENCES employees(id)
    )''')
    
    # 6. Leave Requests Table
    c.execute('''CREATE TABLE IF NOT EXISTS leave_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        leave_type TEXT,
        start_date DATE,
        end_date DATE,
        reason TEXT,
        status TEXT DEFAULT 'Pending',
        manager_id TEXT,
        approved_by TEXT,
        approval_date DATE,
        rejection_reason TEXT
    )''')

    # 7. Payslips Table
    c.execute('''CREATE TABLE IF NOT EXISTS payslips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        month TEXT,
        year INTEGER,
        basic_salary REAL,
        hra REAL,
        special_allowance REAL,
        pf_deduction REAL,
        pt_deduction REAL,
        tds_deduction REAL,
        net_salary REAL,
        generated_date DATE,
        status TEXT DEFAULT 'Generated',
        FOREIGN KEY(employee_id) REFERENCES employees(id)
    )''')

    # 8. Documents Table
    c.execute('''CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        doc_type TEXT,
        file_path TEXT,
        uploaded_date DATE,
        FOREIGN KEY(employee_id) REFERENCES employees(id)
    )''')

    # 9. Assets Table
    c.execute('''CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_type TEXT,
        serial_number TEXT,
        model_name TEXT,
        assigned_to TEXT,
        assigned_date DATE,
        status TEXT DEFAULT 'In Stock',
        FOREIGN KEY(assigned_to) REFERENCES employees(id)
    )''')

    # 10. Separations (Exits) Table
    c.execute('''CREATE TABLE IF NOT EXISTS separations (
        employee_id TEXT PRIMARY KEY,
        resignation_date DATE,
        last_working_day DATE,
        reason TEXT,
        status TEXT DEFAULT 'Pending',
        exit_interview_notes TEXT,
        FOREIGN KEY(employee_id) REFERENCES employees(id)
    )''')
    
    conn.commit()
    conn.close()

def run_query(query, params=()):
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    finally:
        conn.close()

def execute_transaction(operations):
    """
    Executes a list of SQL operations in a single transaction.
    operations: list of tuples (query, params)
    """
    conn = get_connection()
    c = conn.cursor()
    try:
        for query, params in operations:
            c.execute(query, params)
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        st.error(f"Transaction Failed: {e}")
        return False
    finally:
        conn.close()
