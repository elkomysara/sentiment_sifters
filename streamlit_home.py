import streamlit as st


## Setting up the page title and icon
st.set_page_config(page_icon = 'app/sad_happy.jpg',page_title= 'Sentiments Sifter App  ',layout='wide')
# Add a title in the middle of the page using Markdown and CSS
st.markdown("<h1 style='text-align: center;text-decoration: underline;color:GoldenRod'>😀Sentiments Sifter App😠</h1>", unsafe_allow_html=True)
#image wide
st.image("app/sentiments.jpg",use_column_width=True)