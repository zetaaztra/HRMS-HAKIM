import sqlite3
import datetime
from modules import db

def seed_approvals():
    conn = db.get_connection()
    c = conn.cursor()
    
    # Seed 3 Pending Leave Requests
    requests = [
        ("EMP001", "Sick Leave (SL)", "2023-10-10", "2023-10-12", "Viral Fever"),
        ("EMP-DEMO-2", "Unplanned Leave", "2023-10-15", "2023-10-15", "Family Emergency"),
        ("EMP-DEMO-3", "Privilege Leave (PL)", "2023-11-01", "2023-11-05", "Diwali Vacation")
    ]
    
    print("Seeding Pending Leave Requests...")
    for r in requests:
        c.execute("""
            INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, reason, status)
            VALUES (?, ?, ?, ?, ?, 'Pending')
        """, r)
        
    # Seed 1 Pending Resignation
    print("Seeding Pending Resignation...")
    c.execute("""
        INSERT OR IGNORE INTO separations (employee_id, resignation_date, last_working_day, reason, status)
        VALUES (?, ?, ?, ?, 'Pending')
    """, ("EMP-DEMO-EXIT", "2023-10-01", "2023-12-01", "Better Opportunity"))

    # Create dummy employees for these requests if they don't exist
    for emp_id, name in [("EMP-DEMO-2", "Suresh Rain"), ("EMP-DEMO-3", "Anita Desjardins"), ("EMP-DEMO-EXIT", "Rahul Dravid")]:
        c.execute("INSERT OR IGNORE INTO employees (id, name, department, role, salary) VALUES (?, ?, ?, ?, ?)", 
                  (emp_id, name, "Sales", "Manager", 1500000))

    conn.commit()
    conn.close()
    print("Seeding Complete!")

if __name__ == "__main__":
    seed_approvals()
