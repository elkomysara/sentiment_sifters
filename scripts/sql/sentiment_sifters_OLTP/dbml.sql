Project sentiment_sifters {
  database_type: "SQL Server"
}

Table Product {
  product_id INT [primary key, increment]
  asin NVARCHAR(20) [not null, unique]
  product_name NVARCHAR(255) [not null]
  product_type NVARCHAR(100)
}

Table Reviewer {
  reviewer_id INT [primary key, increment]
  reviewer_name NVARCHAR(255) [not null]
  reviewer_location NVARCHAR(255)
  country NVARCHAR(255)
  region NVARCHAR(255)
}

Table Review {
  review_id INT [primary key, increment]
  asin NVARCHAR(20) [not null]
  product_id INT [not null]
  reviewer_id INT [not null]
  helpful_votes INT
  total_votes INT
  rating INT [note: "CHECK (rating BETWEEN 1 AND 5)"]
  review_title NVARCHAR(255)
  review_date DATE
  review_text NVARCHAR(MAX)
  helpful_ratio DECIMAL(5,2) [note: "Persisted Computed Column"]
  sentiment_label NVARCHAR(50)  // Sentiment label column
  sentiment_summary NVARCHAR(MAX)  // Sentiment summary column
  sentiment_score DECIMAL(5,2)  // Sentiment score column
  keyword NVARCHAR(255)  // Keyword column
}

Ref: Review.product_id > Product.product_id
Ref: Review.reviewer_id > Reviewer.reviewer_id
