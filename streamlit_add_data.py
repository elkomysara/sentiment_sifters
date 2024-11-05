import streamlit as st
import pandas as pd
import pyodbc
#import app


# Define the Azure Database connection directly in this file
def get_azure_database_connection():
    """Returns connection to the Azure SQL Database."""
    connection = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"  # Updated driver name
        'Server=tcp:sifters.database.windows.net,1433;'
        'Database=sifters;'  # Azure database name
        'Uid=sifter_login;'  # Azure username
        'Pwd=Sentiment@1990;'  # Replace with the actual password
        'Encrypt=yes;'
        'TrustServerCertificate=no;'
        'Connection Timeout=30;'
    )
    return connection

# Define the `process_single_file` function directly in this file
def process_single_file(file, connection):
    """Processes the uploaded CSV file and inserts it into the Azure database."""
    df = pd.read_csv(file)
    cursor = connection.cursor()

    for index, row in df.iterrows():
        # Example insert query, assuming columns match database table structure
        cursor.execute("""
            INSERT INTO Review (asin, product_id, reviewer_id, helpful_votes, total_votes, rating, 
            review_title, review_date, review_text, sentiment_label, sentiment_summary, sentiment_score, keyword)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            row['asin'], row['product_id'], row['reviewer_id'], row['helpful_votes'], row['total_votes'],
            row['rating'], row['review_title'], row['review_date'], row['review_text'], 
            row['sentiment_label'], row['sentiment_summary'], row['sentiment_score'], row['keyword']
        )
    
    connection.commit()
    cursor.close()

# Streamlit app structure
st.markdown("<h1 style='text-align: center;text-decoration: underline;color:GoldenRod'>Add New Data </h1>", unsafe_allow_html=True)
st.subheader("Sentiment Sifters Data Uploader")

# Step 1: File Upload
st.header("Upload Your CSV")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Step 2: Preview the Uploaded CSV
    df = pd.read_csv(uploaded_file)
    st.write("Preview of the uploaded file:")
    st.dataframe(df.head())

    # Step 3: Process and Insert Data into Azure SQL Database
    if st.button("Upload Data to Database"):
        connection = get_azure_database_connection()
        process_single_file(uploaded_file, connection)
        connection.close()
        st.success("Data successfully uploaded to Azure SQL Database!")
