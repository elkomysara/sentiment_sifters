import streamlit as st

pages= [
st.Page("streamlit_home.py", title="😠Sentiment app Home",icon="😀"),
st.Page("streamlit_about.py", title="About app",icon="📃"),
st.Page("streamlit_dashboard.py", title="Dashboards",icon="📊"),
st.Page("streamlit_add_data.py", title="Adding new review data",icon="📚"),
st.Page("streamlit_sentiment_prediction.py", title="👎Sentiments Sifter", icon="👍")]




ng = st.navigation(pages= pages, position='sidebar', expanded=True)

ng.run()
