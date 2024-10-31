# app/db_setup_azure.py
from app.db_connection_azure import get_azure_database_connection

def create_oltp_and_olap_tables():
    """Creates the OLTP and OLAP tables in the same Azure database if they don't exist."""
    connection = get_azure_database_connection()
    cursor = connection.cursor()

    # Creating OLTP Tables
    print("Creating OLTP tables...")
    
    cursor.execute("""
        IF OBJECT_ID('Product', 'U') IS NULL
        CREATE TABLE Product (
            product_id INT IDENTITY(1,1) PRIMARY KEY,
            asin NVARCHAR(20) NOT NULL UNIQUE,
            product_name NVARCHAR(255) NOT NULL,
            product_type NVARCHAR(100)
        )
    """)
    
    cursor.execute("""
        IF OBJECT_ID('Reviewer', 'U') IS NULL
        CREATE TABLE Reviewer (
            reviewer_id INT IDENTITY(1,1) PRIMARY KEY,
            reviewer_name NVARCHAR(255) NOT NULL,
            reviewer_location NVARCHAR(255),
            country NVARCHAR(255),
            region NVARCHAR(255)
        )
    """)
    
    cursor.execute("""
        IF OBJECT_ID('Review', 'U') IS NULL
        CREATE TABLE Review (
            review_id INT IDENTITY(1,1) PRIMARY KEY,
            asin NVARCHAR(20) NOT NULL,
            product_id INT NOT NULL,
            reviewer_id INT NOT NULL,
            helpful_votes INT,
            total_votes INT,
            rating INT CHECK (rating BETWEEN 1 AND 5),
            review_title NVARCHAR(255),
            review_date DATE,
            review_text NVARCHAR(MAX),
            helpful_ratio AS (CAST(helpful_votes AS DECIMAL(5,2)) / NULLIF(total_votes, 0)) PERSISTED,
            sentiment_label NVARCHAR(50),
            sentiment_summary NVARCHAR(MAX),
            sentiment_score DECIMAL(5,2),
            keyword NVARCHAR(255),
            FOREIGN KEY (product_id) REFERENCES Product(product_id),
            FOREIGN KEY (reviewer_id) REFERENCES Reviewer(reviewer_id)
        )
    """)

    # Creating OLAP Tables
    print("Creating OLAP Dimension and Fact tables...")
    
    cursor.execute("""
        IF OBJECT_ID('DimProduct', 'U') IS NULL
        CREATE TABLE DimProduct (
            ProductKey INT IDENTITY(1,1) PRIMARY KEY,
            asin NVARCHAR(20) NOT NULL UNIQUE,
            product_name NVARCHAR(255),
            product_type NVARCHAR(100)
        )
    """)

    cursor.execute("""
        IF OBJECT_ID('DimReviewer', 'U') IS NULL
        CREATE TABLE DimReviewer (
            ReviewerKey INT IDENTITY(1,1) PRIMARY KEY,
            reviewer_name NVARCHAR(255),
            reviewer_location NVARCHAR(255),
            country NVARCHAR(255),
            region NVARCHAR(255)
        )
    """)

    cursor.execute("""
        IF OBJECT_ID('DimSentiment', 'U') IS NULL
        CREATE TABLE DimSentiment (
            SentimentKey INT IDENTITY(1,1) PRIMARY KEY,
            SentimentLabel NVARCHAR(50),
            SentimentSummary NVARCHAR(MAX),
            SentimentScore DECIMAL(5,2)
        )
    """)

    cursor.execute("""
        IF OBJECT_ID('DimDate', 'U') IS NULL
        CREATE TABLE DimDate (
            DateKey INT IDENTITY(1,1) PRIMARY KEY,
            ReviewDate DATE NOT NULL,
            Year INT,
            Quarter INT,
            Month INT,
            Day INT,
            Weekday INT,
            IsWeekend BIT
        )
    """)

    cursor.execute("""
        IF OBJECT_ID('DimKeyword', 'U') IS NULL
        CREATE TABLE DimKeyword (
            KeywordKey INT IDENTITY(1,1) PRIMARY KEY,
            Keyword NVARCHAR(255)
        )
    """)

    cursor.execute("""
        IF OBJECT_ID('FactReview', 'U') IS NULL
        CREATE TABLE FactReview (
            FactKey INT IDENTITY(1,1) PRIMARY KEY,
            ProductKey INT NOT NULL,
            ReviewerKey INT NOT NULL,
            SentimentKey INT NOT NULL,
            DateKey INT NOT NULL,
            KeywordKey INT,
            HelpfulVotes INT,
            TotalVotes INT,
            HelpfulRatio AS (CAST(HelpfulVotes AS DECIMAL(5,2)) / NULLIF(TotalVotes, 0)) PERSISTED,
            Rating INT CHECK (Rating BETWEEN 1 AND 5),
            ReviewTitle NVARCHAR(255),
            ReviewText NVARCHAR(MAX),
            ReviewDate DATE,
            Year AS YEAR(ReviewDate) PERSISTED,
            Quarter AS (MONTH(ReviewDate) - 1) / 3 + 1 PERSISTED,
            Month AS MONTH(ReviewDate) PERSISTED,
            Day AS DAY(ReviewDate) PERSISTED,
            IsPositiveReview AS (
                CASE WHEN Rating > 3 THEN 1 ELSE 0 END
            ) PERSISTED,
            FOREIGN KEY (ProductKey) REFERENCES DimProduct(ProductKey),
            FOREIGN KEY (ReviewerKey) REFERENCES DimReviewer(ReviewerKey),
            FOREIGN KEY (SentimentKey) REFERENCES DimSentiment(SentimentKey),
            FOREIGN KEY (DateKey) REFERENCES DimDate(DateKey),
            FOREIGN KEY (KeywordKey) REFERENCES DimKeyword(KeywordKey)
        )
    """)

    cursor.commit()
    print("OLTP and OLAP tables created successfully.")
    cursor.close()
    connection.close()


if __name__ == "__main__":
    try:
        connection = get_azure_database_connection()
        print("Connection to Azure SQL Database successful.")
        connection.close()
    except pyodbc.InterfaceError as e:
        print(f"Connection failed: {e}")
