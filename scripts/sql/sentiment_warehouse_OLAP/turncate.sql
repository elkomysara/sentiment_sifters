USE sentiment_warehouse;
GO

-- Disable foreign key constraints on FactReview
ALTER TABLE FactReview NOCHECK CONSTRAINT FK_FactReview_Product;
ALTER TABLE FactReview NOCHECK CONSTRAINT FK_FactReview_Reviewer;
ALTER TABLE FactReview NOCHECK CONSTRAINT FK_FactReview_Sentiment;
ALTER TABLE FactReview NOCHECK CONSTRAINT FK_FactReview_Date;
ALTER TABLE FactReview NOCHECK CONSTRAINT FK_FactReview_Keyword;
GO


USE sentiment_warehouse;
GO-- Drop the FactReview table first
DROP TABLE FactReview;
GO

-- Now drop the dimension tables
DROP TABLE DimKeyword;
DROP TABLE DimSentiment;
DROP TABLE DimDate;
DROP TABLE DimReviewer;
DROP TABLE DimProduct;
GO
