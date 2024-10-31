# app/db_connection_azure.py
import pyodbc

def get_azure_database_connection():
    """Returns connection to the Azure SQL Database (sifters) containing both OLTP and OLAP tables."""
    connection = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"  # Updated driver name
        'Server=tcp:sifters.database.windows.net,1433;'
        'Database=sifters;'  # Main database containing both OLTP and OLAP tables
        'Uid=sifter_login;'  # Azure username
        'Pwd=Sentiment@1990;'  # Replace with the actual password
        'Encrypt=yes;'
        'TrustServerCertificate=no;'
        'Connection Timeout=30;'
    )
    return connection

def get_azure_master_connection():
    """Returns connection to the master database on Azure for administrative tasks."""
    connection = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"  # Updated driver name
        'Server=tcp:sifters.database.windows.net,1433;'
        'Database=master;'
        'Uid=sifter_login;'  # Azure username
        'Pwd=Sentiment@1990;'  # Replace with the actual password
        'Encrypt=yes;'
        'TrustServerCertificate=no;'
        'Connection Timeout=30;'
    )
    return connection
