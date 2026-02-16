import pandas as pd
import streamlit as st
import plotly.express as px

def calculate_attrition_risk(row):
    # Blueprint Formula:
    # Risk = 0.25*(1/SalaryGrowth) + 0.2*LeaveSpike + 0.2*EngagementDrop + 0.2*ManagerChange + 0.15*TenureStage
    # Note: Using the pre-calculated probability from data generator for consistency in demo
    return row.get('Attrition_Probability', 0.0)

def show_attrition_dashboard(df):
    st.markdown("## 🔥 Attrition Risk Predictor")
    
    # High Risk Employees
    high_risk = df[df['Attrition_Probability'] > 0.7].sort_values('Attrition_Probability', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### ⚠️ High Risk Alerts")
        st.dataframe(
            high_risk[['Name', 'Department', 'Role', 'Attrition_Probability', 'Salary_Growth_Ratio']],
            use_container_width=True
        )
    
    with col2:
        st.markdown("### Risk Distribution")
        fig = px.histogram(df, x="Attrition_Probability", nbins=20, title="Risk Score Distribution")
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    # Risk Factors Analysis
    st.markdown("### Key Risk Drivers")
    avg_risk_by_dept = df.groupby('Department')['Attrition_Probability'].mean().reset_index()
    fig2 = px.bar(avg_risk_by_dept, x='Department', y='Attrition_Probability', color='Attrition_Probability',
                 color_continuous_scale='Redor')
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig2, use_container_width=True)

def show_burnout_radar(df):
    st.markdown("## 😓 Burnout Radar")
    
    # Formula: Burnout = (Overtime + NightWork + Meetings) / LeaveTaken
    # Already calculated in generator as 'Burnout_Score'
    
    # Scatter plot of Overtime vs Burnout
    fig = px.scatter(
        df, 
        x='Overtime_Hours', 
        y='Burnout_Score', 
        size='Meeting_Hours',
        color='Department',
        hover_data=['Name'],
        title="Burnout vs. Overtime vs. Meeting Load"
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig, use_container_width=True)
    
    # Burnout Leaderboard
    st.markdown("### Top Burnout Risk Employees")
    top_burnout = df.sort_values('Burnout_Score', ascending=False).head(10)
    st.table(top_burnout[['Name', 'Department', 'Burnout_Score', 'Overtime_Hours', 'Meeting_Hours']])
