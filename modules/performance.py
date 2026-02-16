import streamlit as st
import plotly.express as px

def show_performance_dashboard(df):
    st.markdown("## ⭐ Performance Intelligence")
    
    # Performance vs Salary (Value Matrix)
    fig = px.scatter(
        df, 
        x='Salary', 
        y='Performance_Score', 
        color='Department',
        size='Tenure_Years',
        hover_data=['Name', 'Role'],
        title="Performance vs. Salary (Talent Value Matrix)"
    )
    # Add quadrants lines
    fig.add_hline(y=df['Performance_Score'].mean(), line_dash="dash", line_color="white")
    fig.add_vline(x=df['Salary'].mean(), line_dash="dash", line_color="white")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Top Performers")
        top_performers = df.sort_values('Performance_Score', ascending=False).head(5)
        for _, row in top_performers.iterrows():
            st.success(f"**{row['Name']}** ({row['Role']}) - Score: {row['Performance_Score']}")
            
    with col2:
        st.markdown("### 📉 Underperformers (Action Needed)")
        low_performers = df.sort_values('Performance_Score', ascending=True).head(5)
        for _, row in low_performers.iterrows():
            st.error(f"**{row['Name']}** ({row['Role']}) - Score: {row['Performance_Score']}")

