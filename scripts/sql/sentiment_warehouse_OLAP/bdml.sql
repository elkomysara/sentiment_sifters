Project sentiment_warehouse {
  database_type: "SQL Server"
}

Table DimProduct {
  ProductKey INT [primary key, increment]
  asin NVARCHAR(20) [not null, unique]
  product_name NVARCHAR(255)
  product_type NVARCHAR(100)
}

Table DimReviewer {
  ReviewerKey INT [primary key, increment]
  reviewer_name NVARCHAR(255)
  reviewer_location NVARCHAR(255)
  country NVARCHAR(255)
  region NVARCHAR(255)
}

Table DimSentiment {
  SentimentKey INT [primary key, increment]
  SentimentLabel NVARCHAR(50)
  SentimentSummary NVARCHAR(MAX)
  SentimentScore DECIMAL(5,2)
}

Table DimDate {
  DateKey INT [primary key, increment]
  ReviewDate DATE
  Year INT
  Quarter INT
  Month INT
  Day INT
  Weekday INT
  IsWeekend BIT
  IsHoliday BIT
  IsBlackFriday BIT
  IsChristmas BIT
}

Table DimKeyword {
  KeywordKey INT [primary key, increment]
  Keyword NVARCHAR(255)
}

Table FactReview {
  FactKey INT [primary key, increment]
  ProductKey INT [not null, ref: > DimProduct.ProductKey]
  ReviewerKey INT [not null, ref: > DimReviewer.ReviewerKey]
  SentimentKey INT [not null, ref: > DimSentiment.SentimentKey]
  DateKey INT [not null, ref: > DimDate.DateKey]
  KeywordKey INT [ref: > DimKeyword.KeywordKey]
  HelpfulVotes INT
  TotalVotes INT
  HelpfulRatio DECIMAL(5,2)
  Rating INT [note: "CHECK (Rating BETWEEN 1 AND 5)"]
  ReviewTitle NVARCHAR(255)
  ReviewText NVARCHAR(MAX)
  ReviewDate DATE
}
