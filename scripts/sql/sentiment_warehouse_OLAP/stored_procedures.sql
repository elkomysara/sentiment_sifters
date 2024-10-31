USE sentiment_warehouse;
GO
-- Insert into DimKeyword
CREATE OR ALTER PROCEDURE sp_InsertDimKeyword
    @Keyword NVARCHAR(255),
    @KeywordKey INT OUTPUT
AS
BEGIN
    -- If the keyword already exists, fetch its KeywordKey, else insert and return new KeywordKey
    IF EXISTS (SELECT 1 FROM DimKeyword WHERE Keyword = @Keyword)
    BEGIN
        SELECT @KeywordKey = KeywordKey FROM DimKeyword WHERE Keyword = @Keyword;
    END
    ELSE
    BEGIN
        INSERT INTO DimKeyword (Keyword)
        VALUES (@Keyword);
        SET @KeywordKey = SCOPE_IDENTITY();
    END
END;
GO

-- Insert into DimProduct
CREATE OR ALTER PROCEDURE sp_InsertDimProduct
    @asin NVARCHAR(20),  
    @product_name NVARCHAR(255),  
    @product_type NVARCHAR(100),
    @ProductKey INT OUTPUT  
AS
BEGIN
    -- If the product already exists, fetch its ProductKey, else insert and return new ProductKey
    IF EXISTS (SELECT 1 FROM DimProduct WHERE asin = @asin)
    BEGIN
        SELECT @ProductKey = ProductKey FROM DimProduct WHERE asin = @asin;
    END
    ELSE
    BEGIN
        INSERT INTO DimProduct (asin, product_name, product_type)
        VALUES (@asin, @product_name, @product_type);
        SET @ProductKey = SCOPE_IDENTITY();
    END
END;
GO

CREATE OR ALTER PROCEDURE sp_InsertDimProduct
    @asin NVARCHAR(20),  
    @product_name NVARCHAR(255),  
    @product_type NVARCHAR(100),
    @ProductKey INT OUTPUT  
AS
BEGIN
    IF EXISTS (SELECT 1 FROM DimProduct WHERE asin = @asin)
    BEGIN
        SELECT @ProductKey = ProductKey FROM DimProduct WHERE asin = @asin;
        PRINT 'Product exists. ProductKey: ' + CAST(@ProductKey AS NVARCHAR(50));
    END
    ELSE
    BEGIN
        INSERT INTO DimProduct (asin, product_name, product_type)
        VALUES (@asin, @product_name, @product_type);
        SET @ProductKey = SCOPE_IDENTITY();
        PRINT 'New product inserted. ProductKey: ' + CAST(@ProductKey AS NVARCHAR(50));
    END
END;
GO


-- Insert into DimReviewer
CREATE OR ALTER PROCEDURE sp_InsertDimReviewer
    @reviewer_name NVARCHAR(255),  
    @reviewer_location NVARCHAR(255),  
    @country NVARCHAR(255),  
    @region NVARCHAR(255),
    @ReviewerKey INT OUTPUT  
AS
BEGIN
    -- If the reviewer already exists, fetch their ReviewerKey, else insert and return new ReviewerKey
    IF EXISTS (SELECT 1 FROM DimReviewer WHERE reviewer_name = @reviewer_name)
    BEGIN
        SELECT @ReviewerKey = ReviewerKey FROM DimReviewer WHERE reviewer_name = @reviewer_name;
    END
    ELSE
    BEGIN
        INSERT INTO DimReviewer (reviewer_name, reviewer_location, country, region)
        VALUES (@reviewer_name, @reviewer_location, @country, @region);
        SET @ReviewerKey = SCOPE_IDENTITY();
    END
END;
GO

-- Insert into DimSentiment
CREATE OR ALTER PROCEDURE sp_InsertDimSentiment
    @SentimentLabel NVARCHAR(50),  
    @SentimentSummary NVARCHAR(MAX),  
    @SentimentScore DECIMAL(5,2),
    @SentimentKey INT OUTPUT  
AS
BEGIN
    -- If the sentiment already exists, fetch its SentimentKey, else insert and return new SentimentKey
    IF EXISTS (SELECT 1 FROM DimSentiment WHERE SentimentLabel = @SentimentLabel AND SentimentScore = @SentimentScore)
    BEGIN
        SELECT @SentimentKey = SentimentKey FROM DimSentiment WHERE SentimentLabel = @SentimentLabel AND SentimentScore = @SentimentScore;
    END
    ELSE
    BEGIN
        INSERT INTO DimSentiment (SentimentLabel, SentimentSummary, SentimentScore)
        VALUES (@SentimentLabel, @SentimentSummary, @SentimentScore);
        SET @SentimentKey = SCOPE_IDENTITY();
    END
END;
GO

-- Insert into DimDate
CREATE OR ALTER PROCEDURE sp_InsertDimDate
    @ReviewDate DATE,
    @DateKey INT OUTPUT
AS
BEGIN
    -- If the date already exists, fetch its DateKey, else insert and return new DateKey
    IF EXISTS (SELECT 1 FROM DimDate WHERE ReviewDate = @ReviewDate)
    BEGIN
        SELECT @DateKey = DateKey FROM DimDate WHERE ReviewDate = @ReviewDate;
    END
    ELSE
    BEGIN
        DECLARE @Year INT = YEAR(@ReviewDate);
        DECLARE @Quarter INT = (MONTH(@ReviewDate) - 1) / 3 + 1;
        DECLARE @Month INT = MONTH(@ReviewDate);
        DECLARE @Day INT = DAY(@ReviewDate);
        DECLARE @Weekday INT = DATEPART(WEEKDAY, @ReviewDate);
        DECLARE @IsWeekend BIT = CASE WHEN @Weekday IN (1, 7) THEN 1 ELSE 0 END;
        DECLARE @IsHoliday BIT = 0;
        DECLARE @IsBlackFriday BIT = CASE WHEN @Month = 11 AND @Weekday = 6 AND @Day BETWEEN 23 AND 29 THEN 1 ELSE 0 END;
        DECLARE @IsChristmas BIT = CASE WHEN @Month = 12 AND @Day = 25 THEN 1 ELSE 0 END;

        INSERT INTO DimDate (ReviewDate, Year, Quarter, Month, Day, Weekday, IsWeekend, IsHoliday, IsBlackFriday, IsChristmas)
        VALUES (@ReviewDate, @Year, @Quarter, @Month, @Day, @Weekday, @IsWeekend, @IsHoliday, @IsBlackFriday, @IsChristmas);

        SET @DateKey = SCOPE_IDENTITY();
    END
END;
GO


-- Corrected Insert into FactReview to handle keyword key and correct parameter count
CREATE OR ALTER PROCEDURE sp_InsertFactReview
    @ProductKey INT,
    @ReviewerKey INT,
    @SentimentKey INT,
    @DateKey INT,
    @KeywordKey INT = NULL,  -- Made optional for cases where no keyword is provided
    @HelpfulVotes INT,
    @TotalVotes INT,
    @Rating INT,
    @ReviewTitle NVARCHAR(255),
    @ReviewText NVARCHAR(MAX)
AS
BEGIN
    -- Validate that none of the foreign keys are NULL
    IF @ProductKey IS NULL OR @ReviewerKey IS NULL OR @SentimentKey IS NULL OR @DateKey IS NULL
    BEGIN
        -- If any required key is NULL, return an error
        RAISERROR('Cannot insert into FactReview because one or more foreign keys are NULL.', 16, 1);
        RETURN;
    END;

    -- Insert into FactReview table
    INSERT INTO FactReview 
        (ProductKey, ReviewerKey, SentimentKey, DateKey, KeywordKey, HelpfulVotes, TotalVotes, Rating, ReviewTitle, ReviewText)
    VALUES
        (@ProductKey, @ReviewerKey, @SentimentKey, @DateKey, @KeywordKey, @HelpfulVotes, @TotalVotes, @Rating, @ReviewTitle, @ReviewText);
END;
GO
