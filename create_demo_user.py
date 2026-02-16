import sqlite3
import pandas as pd
from modules import db

def create_demo_user():
    conn = db.get_connection()
    c = conn.cursor()
    
    emp_id = "EMP001"
    name = "Rajesh Demo"
    
    print(f"Creating Demo User: {emp_id} / password ...")
    
    # 1. Employee
    c.execute("INSERT OR REPLACE INTO employees (id, name, department, role, joining_date, email, mobile, salary) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (emp_id, name, "Engineering", "Senior Dev", "2023-01-01", "rajesh@demo.com", "9999999999", 2500000))
    
    # 2. Compliance
    c.execute("INSERT OR REPLACE INTO compliance (employee_id, pan_number, aadhar_number) VALUES (?, ?, ?)",
              (emp_id, "ABCDE1234F", "123412341234"))
    
    # 3. Attendance (7 days)
    for i in range(7):
        date = (pd.Timestamp.now() - pd.Timedelta(days=i)).date()
        c.execute("INSERT INTO attendance (employee_id, date, status, check_in, check_out, hours_worked) VALUES (?, ?, ?, ?, ?, ?)",
                  (emp_id, date, "Present", "09:00", "18:00", 9.0))
        
    conn.commit()
    conn.close()
    print("Success! Login with User: EMP001 | Pass: password")

if __name__ == "__main__":
    create_demo_user()
