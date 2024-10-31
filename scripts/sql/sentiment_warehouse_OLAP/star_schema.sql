USE sentiment_warehouse;
GO

-- -- Drop existing tables if they exist
-- IF OBJECT_ID('DimProduct', 'U') IS NOT NULL DROP TABLE DimProduct;
-- IF OBJECT_ID('DimReviewer', 'U') IS NOT NULL DROP TABLE DimReviewer;
-- IF OBJECT_ID('DimSentiment', 'U') IS NOT NULL DROP TABLE DimSentiment;
-- IF OBJECT_ID('DimDate', 'U') IS NOT NULL DROP TABLE DimDate;
-- IF OBJECT_ID('DimKeyword', 'U') IS NOT NULL DROP TABLE DimKeyword;
-- IF OBJECT_ID('FactReview', 'U') IS NOT NULL DROP TABLE FactReview;
-- GO

-- Create DimProduct table
CREATE TABLE DimProduct (
    ProductKey INT IDENTITY(1,1) PRIMARY KEY,
    asin NVARCHAR(20) NOT NULL UNIQUE,
    product_name NVARCHAR(255),
    product_type NVARCHAR(100)
);
GO

-- Create DimReviewer table
CREATE TABLE DimReviewer (
    ReviewerKey INT IDENTITY(1,1) PRIMARY KEY,
    reviewer_name NVARCHAR(255),
    reviewer_location NVARCHAR(255),
    country NVARCHAR(255),
    region NVARCHAR(255)
);
GO

-- Create DimSentiment table
CREATE TABLE DimSentiment (
    SentimentKey INT IDENTITY(1,1) PRIMARY KEY,
    SentimentLabel NVARCHAR(50),
    SentimentSummary NVARCHAR(MAX),
    SentimentScore DECIMAL(5,2)
);
GO

-- Create DimDate table
CREATE TABLE DimDate (
    DateKey INT IDENTITY(1,1) PRIMARY KEY,
    ReviewDate DATE NOT NULL,
    Year INT,
    Quarter INT,
    Month INT,
    Day INT,
    Weekday INT,
    IsWeekend BIT,
    IsHoliday BIT,
    IsBlackFriday BIT,
    IsChristmas BIT
);
GO

-- Create DimKeyword table
CREATE TABLE DimKeyword (
    KeywordKey INT IDENTITY(1,1) PRIMARY KEY,
    Keyword NVARCHAR(255)
);
GO
USE sentiment_warehouse;
GO
-- Create FactReview table
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
    CONSTRAINT FK_FactReview_Product FOREIGN KEY (ProductKey) REFERENCES DimProduct(ProductKey),
    CONSTRAINT FK_FactReview_Reviewer FOREIGN KEY (ReviewerKey) REFERENCES DimReviewer(ReviewerKey),
    CONSTRAINT FK_FactReview_Sentiment FOREIGN KEY (SentimentKey) REFERENCES DimSentiment(SentimentKey),
    CONSTRAINT FK_FactReview_Date FOREIGN KEY (DateKey) REFERENCES DimDate(DateKey),
    CONSTRAINT FK_FactReview_Keyword FOREIGN KEY (KeywordKey) REFERENCES DimKeyword(KeywordKey)
);
GO
