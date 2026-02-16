import streamlit as st
import pandas as pd
from faker import Faker
import random

fake = Faker()

def generate_candidates(n=10):
    candidates = []
    for _ in range(n):
        skill_match = random.uniform(0.5, 1.0)
        exp_score = random.uniform(0.5, 1.0)
        culture_fit = random.uniform(0.5, 1.0)
        stability_score = random.uniform(0.5, 1.0)
        
        # Fit Probability Formula
        fit_score = skill_match * exp_score * culture_fit * stability_score
        
        candidates.append({
            'Name': fake.name(),
            'Role_Applied': random.choice(['Senior Engineer', 'Product Manager', 'HR BP']),
            'Skill_Match': round(skill_match, 2),
            'Experience_Score': round(exp_score, 2),
            'Culture_Fit': round(culture_fit, 2),
            'Stability_Score': round(stability_score, 2),
            'AI_Fit_Score': round(fit_score, 2)
        })
    return pd.DataFrame(candidates)

def show_recruitment_dashboard():
    st.markdown("## 🧠 AI Recruitment Intelligence")
    
    if 'candidates' not in st.session_state:
        st.session_state.candidates = generate_candidates(15)
        
    df = st.session_state.candidates
    
    # Filter by role
    role = st.selectbox("Select Role Pipeline", df['Role_Applied'].unique())
    filtered_df = df[df['Role_Applied'] == role].sort_values('AI_Fit_Score', ascending=False)
    
    st.markdown(f"### Top Candidates for {role}")
    
    for i, row in filtered_df.iterrows():
        with st.expander(f"{row['Name']} (AI Score: {row['AI_Fit_Score']})"):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Skill Match", f"{row['Skill_Match']*100:.0f}%")
            c2.metric("Experience", f"{row['Experience_Score']*100:.0f}%")
            c3.metric("Culture Fit", f"{row['Culture_Fit']*100:.0f}%")
            c4.metric("Stability", f"{row['Stability_Score']*100:.0f}%")
            
            if row['AI_Fit_Score'] > 0.6:
                st.button(f"Schedule Interview for {row['Name']}", key=f"btn_{i}")
            else:
                st.warning("Low Fit Probability - Not Recommended")
