
-- Switch to the sentiment_sifters database
USE sentiment_sifters;
GO

-- Recreate the Product table (with asin)
CREATE TABLE Product (
    product_id INT IDENTITY(1,1) PRIMARY KEY,
    asin NVARCHAR(20) NOT NULL UNIQUE,  
    product_name NVARCHAR(255) NOT NULL,  
    product_type NVARCHAR(100)
);
GO

-- Recreate the Reviewer table
CREATE TABLE Reviewer (
    reviewer_id INT IDENTITY(1,1) PRIMARY KEY,
    reviewer_name NVARCHAR(255) NOT NULL,  
    reviewer_location NVARCHAR(255),  
    country NVARCHAR(255),  
    region NVARCHAR(255)
);
GO

-- Recreate the Review table with added sentiment and keyword columns
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
    sentiment_label NVARCHAR(50),  -- Added sentiment label
    sentiment_summary NVARCHAR(MAX),  -- Added sentiment summary
    sentiment_score DECIMAL(5,2),  -- Added sentiment score
    keyword NVARCHAR(255),  -- Added keyword
    CONSTRAINT FK_Review_Product FOREIGN KEY (product_id) REFERENCES Product(product_id),
    CONSTRAINT FK_Review_Reviewer FOREIGN KEY (reviewer_id) REFERENCES Reviewer(reviewer_id)
);
GO
