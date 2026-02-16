import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/employee_metrics.csv")
        # Ensure dates are datetime
        df['Joining_Date'] = pd.to_datetime(df['Joining_Date'])
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please run data_generator.py first.")
        return pd.DataFrame()

def get_department_metrics(df):
    return df.groupby('Department').agg({
        'Employee_ID': 'count',
        'Salary': 'mean',
        'Attrition_Probability': 'mean'
    }).rename(columns={
        'Employee_ID': 'Headcount',
        'Salary': 'Avg Salary',
        'Attrition_Probability': 'Avg Attrition Risk'
    })

def filter_by_department(df, department):
    if department == "All":
        return df
    return df[df['Department'] == department]
