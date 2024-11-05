# streamlit_app/streamlit_app.py
import streamlit as st


st.set_page_config(page_title= 'Dashboard  ')

st.image("app/dashboard.png")

st.markdown("<h1 style='text-align: center;text-decoration: underline;color:GoldenRod'>Dashboard</h1>", unsafe_allow_html=True)
# Step 4: Display Power BI Report
st.header("Power BI Report")
power_bi_url = "https://app.powerbi.com/view?r=eyJrIjoiZGI1ZmQ5N2MtMmE1Zi00ZjFhLWJlZjctMTM0ZjIxNTEzMDM5IiwidCI6ImY4NGExNjNjLWRhNWYtNGU3Ni1iNDdhLWFmNTRlZDY5NmI1ZSJ9"  # Power BI  Web link

st.markdown(f"""
    <iframe width="1000" height="700" src="{power_bi_url}" frameborder="0" allowFullScreen="true"></iframe>
""", unsafe_allow_html=True)

