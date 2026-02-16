import streamlit as st
import pandas as pd
import plotly.express as px
import random

def generate_sentiment_data():
    dates = pd.date_range(start="2023-01-01", periods=12, freq='M')
    sentiment = [random.uniform(3.5, 4.8) for _ in range(12)]
    return pd.DataFrame({"Date": dates, "Sentiment": sentiment})

def show_engagement_dashboard():
    st.markdown("## 😃 Employee Experience Engine")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Organizational Mood Tracker")
        try:
            df = generate_sentiment_data()
            fig = px.line(df, x='Date', y='Sentiment', title="Company Sentiment Trend")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error generating sentiment data: {e}")
            
    with col2:
        st.markdown("### Recent Feedback Pulse")
        st.info("💬 'Great team spirit, but meetings are overwhelming.' - Engineering")
        st.success("💬 'Loving the new learning budget!' - Marketing")
        st.warning("💬 'Need better coffee in the breakroom.' - Sales")
        
    st.markdown("### Engagement Score Formula")
    st.latex(r'''
        Engagement = Sentiment + Participation + Learning + FeedbackScore
    ''')
