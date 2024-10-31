-- Switch to the sentiment_sifters database
USE sentiment_sifters;
GO


-- Drop all tables if they exist
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'Keyword')
    DROP TABLE Keyword;
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'Sentiment')
    DROP TABLE Sentiment;
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'Review')
    DROP TABLE Review;
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'Product')
    DROP TABLE Product;
IF EXISTS (SELECT * FROM sys.tables WHERE name = 'Reviewer')
    DROP TABLE Reviewer;
GO
-- Drop all stored procedures if they exist
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_InsertProduct')
    DROP PROCEDURE sp_InsertProduct;
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_InsertReviewer')
    DROP PROCEDURE sp_InsertReviewer;
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_InsertReview')
    DROP PROCEDURE sp_InsertReview;
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_InsertSentiment')
    DROP PROCEDURE sp_InsertSentiment;
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_InsertKeyword')
    DROP PROCEDURE sp_InsertKeyword;
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_GetReviewWithSentimentsAndKeywords')
    DROP PROCEDURE sp_GetReviewWithSentimentsAndKeywords;
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_GetReviewerInfo')
    DROP PROCEDURE sp_GetReviewerInfo;