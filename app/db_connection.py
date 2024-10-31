# app/db_connection.py
import pyodbc

def get_oltp_connection():
    """Returns connection to the OLTP (sentiment_sifters) database."""
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-4U8DFLK;'
        'DATABASE=sentiment_sifters;'
        'UID=sifter_login;PWD=sifter_login'
    )
    return connection

def get_olap_connection():
    """Returns connection to the OLAP (sentiment_warehouse) database."""
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-4U8DFLK;'
        'DATABASE=sentiment_warehouse;'
        'UID=sifter_login;PWD=sifter_login'
    )
    return connection

def get_master_connection():
    """Returns connection to the master database for creating other databases."""
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-4U8DFLK;'
        'DATABASE=master;'
        'UID=sifter_login;PWD=sifter_login'
    )
    return connection

