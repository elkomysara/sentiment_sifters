
-- Switch to the sentiment_sifters database
USE sentiment_sifters;
GO

-- Insert into Product table
CREATE OR ALTER PROCEDURE sp_InsertProduct
    @asin NVARCHAR(20),  
    @product_name NVARCHAR(255),  
    @product_type NVARCHAR(100)  
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Product WHERE asin = @asin)
    BEGIN
        INSERT INTO Product (asin, product_name, product_type)
        VALUES (@asin, @product_name, @product_type);
    END
END;
GO

-- Insert into Reviewer table
CREATE OR ALTER PROCEDURE sp_InsertReviewer
    @reviewer_name NVARCHAR(255),  
    @reviewer_location NVARCHAR(255),  
    @country NVARCHAR(255),  
    @region NVARCHAR(255)  
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Reviewer WHERE reviewer_name = @reviewer_name)
    BEGIN
        INSERT INTO Reviewer (reviewer_name, reviewer_location, country, region)
        VALUES (@reviewer_name, @reviewer_location, @country, @region);
    END
END;
GO

-- Insert into Review table, including sentiment and keyword columns
CREATE OR ALTER PROCEDURE sp_InsertReview
    @asin NVARCHAR(20),  
    @product_id INT,
    @reviewer_id INT,
    @helpful_votes INT,
    @total_votes INT,
    @rating INT,
    @review_title NVARCHAR(255),  
    @review_date DATE,
    @review_text NVARCHAR(MAX),
    @sentiment_label NVARCHAR(50),  -- New parameter for sentiment label
    @sentiment_summary NVARCHAR(MAX),  -- New parameter for sentiment summary
    @sentiment_score DECIMAL(5,2),  -- New parameter for sentiment score
    @keyword NVARCHAR(255)  -- New parameter for keyword
AS
BEGIN
    INSERT INTO Review (
        asin, product_id, reviewer_id, helpful_votes, total_votes, rating, review_title, review_date, review_text,
        sentiment_label, sentiment_summary, sentiment_score, keyword)  -- Insert sentiment and keyword data
    VALUES (
        @asin, @product_id, @reviewer_id, @helpful_votes, @total_votes, @rating, @review_title, @review_date, @review_text,
        @sentiment_label, @sentiment_summary, @sentiment_score, @keyword);  -- Insert sentiment and keyword data
END;
GO

-- Retrieve Reviews along with Sentiments and Keywords (now all part of the Review table)
CREATE OR ALTER PROCEDURE sp_GetReviewWithSentimentsAndKeywords
AS
BEGIN
    SELECT 
        review_id, 
        asin, 
        review_title, 
        review_date, 
        review_text, 
        rating, 
        sentiment_label,  -- Sentiment information
        sentiment_summary,  -- Sentiment summary
        sentiment_score,  -- Sentiment score
        keyword  -- Keyword information
    FROM Review;
END;
GO

-- Retrieve Reviewer Information
CREATE OR ALTER PROCEDURE sp_GetReviewerInfo
AS
BEGIN
    SELECT 
        reviewer_id, 
        reviewer_name, 
        reviewer_location, 
        country, 
        region
    FROM Reviewer;
END;
GO
