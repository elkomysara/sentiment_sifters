USE sentiment_warehouse;

-- Test DimProduct Insert
INSERT INTO DimProduct (asin, product_name, product_type)
VALUES ('B001E4KFG0', 'Sample Product', 'Electronics');
SELECT SCOPE_IDENTITY() AS ProductKey;

-- Test DimReviewer Insert
INSERT INTO DimReviewer (reviewer_name, reviewer_location, country, region)
VALUES ('John Doe', 'NY', 'USA', 'NY');
SELECT SCOPE_IDENTITY() AS ReviewerKey;

-- Test DimSentiment Insert
INSERT INTO DimSentiment (SentimentLabel, SentimentSummary, SentimentScore)
VALUES ('POSITIVE', 'Great product', 0.95);
SELECT SCOPE_IDENTITY() AS SentimentKey;
