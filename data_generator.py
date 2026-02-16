import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

def generate_employee_data(num_employees=250):
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Product']
    roles = ['Junior', 'Senior', 'Manager', 'Director', 'VP']
    locations = ['Bangalore', 'Mumbai', 'Delhi', 'Remote']
    
    data = []
    
    for _ in range(num_employees):
        dept = random.choice(departments)
        role = random.choice(roles)
        salary_base = {
            'Junior': (500000, 1000000),
            'Senior': (1200000, 2500000),
            'Manager': (2000000, 4000000),
            'Director': (4000000, 8000000),
            'VP': (8000000, 15000000)
        }
        
        salary = random.randint(*salary_base[role])
        joining_date = fake.date_between(start_date='-5y', end_date='today')
        
        # Risk Factors
        salary_growth = random.uniform(0.8, 1.5) # < 1 means effective decrease due to inflation/market
        leave_spike = random.choice([0, 1]) if random.random() > 0.8 else 0
        engagement_score = random.randint(1, 10)
        manager_change = random.choice([0, 1]) if random.random() > 0.9 else 0
        tenure_years = (pd.Timestamp.now().date() - joining_date).days / 365
        tenure_stage = 1 if tenure_years > 3 else 0 # Higher risk after 3 years often
        
        # Performance
        output_score = random.randint(1, 10)
        consistency_score = random.randint(1, 10)
        peer_score = random.randint(1, 10)
        goal_score = random.randint(1, 10)
        learning_score = random.randint(1, 10)

        # Burnout Factors
        overtime_hours = random.randint(0, 20)
        night_work_hours = random.randint(0, 10)
        meeting_hours = random.randint(5, 25)
        leaves_taken = random.randint(1, 20)
        
        employee = {
            'Employee_ID': fake.uuid4()[:8],
            'Name': fake.name(),
            'Department': dept,
            'Role': role,
            'Location': random.choice(locations),
            'Joining_Date': joining_date,
            'Salary': salary,
            'Manager_ID': fake.uuid4()[:8],
            # Attrition Inputs
            'Salary_Growth_Ratio': round(salary_growth, 2),
            'Leave_Spike': leave_spike,
            'Engagement_Score': engagement_score,
            'Manager_Change': manager_change,
            'Tenure_Years': round(tenure_years, 1),
            # Performance Inputs
            'Output_Score': output_score,
            'Consistency_Score': consistency_score,
            'Peer_Score': peer_score,
            'Goal_Score': goal_score,
            'Learning_Score': learning_score,
            # Burnout Inputs
            'Overtime_Hours': overtime_hours,
            'Night_Work_Hours': night_work_hours,
            'Meeting_Hours': meeting_hours,
            'Leaves_Taken': leaves_taken
        }
        data.append(employee)
        
    df = pd.DataFrame(data)
    
    # Calculate Attrition Risk (Logic from Blueprint)
    # Risk = 0.25*(1/SalaryGrowth) - 1 + 0.2*LeaveSpike + 0.2*LowEngagement + ...
    # Normalized for 0-1 scale mostly, keeping it simple for demo
    # Note: Blueprint formula: 0.25*SalaryGrowth - 1 ... wait, 
    # Blueprint says: Risk = 0.25 * SalaryGrowth - 1 + ... 
    # Let's use a slightly modified robust formula for the data generation to ensure valid spread
    
    def calc_risk(row):
        # Inverting growth: low growth = high risk
        risk = (
            0.3 * (1.5 - row['Salary_Growth_Ratio']) + 
            0.2 * row['Leave_Spike'] + 
            0.2 * ((10 - row['Engagement_Score'])/10) + 
            0.2 * row['Manager_Change'] + 
            0.1 * (1 if row['Tenure_Years'] > 2 and row['Tenure_Years'] < 5 else 0)
        )
        return min(max(risk, 0), 1) # Clip between 0 and 1

    df['Attrition_Probability'] = df.apply(calc_risk, axis=1)
    
    # Calculate Performance Score
    # Score = 0.3*Output + 0.2*Consistency + 0.2*Peer + 0.2*Goal + 0.1*Learning
    df['Performance_Score'] = (
        0.3 * df['Output_Score'] + 
        0.2 * df['Consistency_Score'] + 
        0.2 * df['Peer_Score'] + 
        0.2 * df['Goal_Score'] + 
        0.1 * df['Learning_Score']
    ).round(1)

    # Calculate Burnout Score
    # Burnout = (Overtime + NightWork + Meetings) / LeaveTaken
    # Managing div by zero
    df['Burnout_Score'] = (
        (df['Overtime_Hours'] + df['Night_Work_Hours'] + df['Meeting_Hours']) / 
        df['Leaves_Taken'].replace(0, 1)
    ).round(1)

    return df

if __name__ == "__main__":
    print("Generating employee data...")
    df = generate_employee_data(250)
    df.to_csv("data/employee_metrics.csv", index=False)
    print(f"Generated {len(df)} employee records in data/employee_metrics.csv")
