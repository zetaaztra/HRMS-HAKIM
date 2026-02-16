import pandas as pd
import sqlite3
from modules import db
from faker import Faker
import random

fake = Faker()

def migrate_data():
    print("Initializing Database...")
    db.init_db()
    
    try:
        df = pd.read_csv("data/employee_metrics.csv")
        print(f"Found {len(df)} records in CSV. Migrating to SQLite...")
        
        ops_emp = []
        ops_comp = []
        ops_bank = []
        ops_addr = []
        
        conn = db.get_connection()
        c = conn.cursor()
        
        for _, row in df.iterrows():
            emp_id = str(row['Employee_ID'])
            name = row['Name']
            
            # Employee Base
            ops_emp.append((
                "INSERT OR IGNORE INTO employees (id, name, department, role, joining_date, salary) VALUES (?, ?, ?, ?, ?, ?)",
                (emp_id, name, row['Department'], row['Role'], row['Joining_Date'], row['Salary'])
            ))
            
            # Random Indian Compliance Data
            pan = fake.bothify(text='?????####?').upper()
            aadhar = fake.numerify(text='############')
            uan = fake.numerify(text='1009#######')
            
            ops_comp.append((
                "INSERT OR REPLACE INTO compliance (employee_id, pan_number, aadhar_number, uan_number) VALUES (?, ?, ?, ?)",
                (emp_id, pan, aadhar, uan)
            ))
            
            # Random Banking
            bank = random.choice(['HDFC Bank', 'ICICI Bank', 'SBI', 'Axis Bank'])
            acct = fake.numerify(text='##########')
            ifsc = bank[:4].upper() + "000" + fake.numerify(text='####')
            
            ops_bank.append((
                "INSERT OR REPLACE INTO banking (employee_id, bank_name, account_number, ifsc_code) VALUES (?, ?, ?, ?)",
                (emp_id, bank, acct, ifsc)
            ))
            
            # Random Address
            ops_addr.append((
                "INSERT OR REPLACE INTO addresses (employee_id, current_address, city, state) VALUES (?, ?, ?, ?)",
                (emp_id, fake.address(), row['Location'], "Karnataka")
            ))
            
            # Dummy Attendance (Last 7 days)
            for i in range(7):
                date = (pd.Timestamp.now() - pd.Timedelta(days=i)).date()
                status = random.choice(['Present', 'Present', 'Present', 'Absent', 'Leave'])
                check_in = "09:00" if status == 'Present' else None
                check_out = "18:00" if status == 'Present' else None
                hours = 9.0 if status == 'Present' else 0
                
                c.execute(
                    "INSERT INTO attendance (employee_id, date, status, check_in, check_out, hours_worked) VALUES (?, ?, ?, ?, ?, ?)",
                    (emp_id, date, status, check_in, check_out, hours)
                )

        # Execute Batch
        c.executemany(ops_emp[0][0], [x[1] for x in ops_emp])
        c.executemany(ops_comp[0][0], [x[1] for x in ops_comp])
        c.executemany(ops_bank[0][0], [x[1] for x in ops_bank])
        c.executemany(ops_addr[0][0], [x[1] for x in ops_addr])
        
        conn.commit()
        conn.close()
        print("Migration Complete!")
        
    except FileNotFoundError:
        print("No CSV found. Database initialized empty.")

if __name__ == "__main__":
    migrate_data()
