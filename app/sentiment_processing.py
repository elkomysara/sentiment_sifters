import logging
import mlflow
import mlflow.pyfunc
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from app.db_connection import get_oltp_connection  # Using OLTP for sentiment analysis
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import re

# Initialize pipelines outside functions for reuse
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", revision="714eb0f")

# Simplified keyword extraction, avoiding stopwords and trivial words
def extract_keywords(text):
    stopwords = set(["the", "is", "in", "at", "of", "and", "a", "an", "to", "for", "on", "it", "this", "that"])  # Add more common words
    words = re.findall(r'\b\w+\b', text.lower())  # Extract words
    keywords = [word for word in words if word not in stopwords and len(word) > 2]  # Filter out stopwords and short words
    return ' '.join(keywords[:2])  # Limit to 2 keywords

# Sentiment analysis function
def perform_sentiment_analysis(text):
    max_length = 512
    truncated_text = text[:max_length]
    try:
        result = sentiment_pipeline(truncated_text)[0]
        sentiment_label = result['label']
        sentiment_score = result['score']
        return sentiment_label, sentiment_score
    except Exception as e:
        logging.error(f"Sentiment analysis failed: {e}")
        raise e

# Simplified summary generation using the title
def summarize_text_using_title(title):
    try:
        summary = title[:50]  # Truncate the title to a max length of 50 characters as a simplified summary
        return summary
    except Exception as e:
        logging.error(f"Summary generation failed: {e}")
        raise e

# Function to process a single review
def process_single_review(review):
    review_id, review_text, rating, review_title = review
    combined_text = f"{review_text} {rating} {review_title}"

    try:
        start_time = time.time()  # Start time for each row
        sentiment_label, sentiment_score = perform_sentiment_analysis(combined_text)
        keyword = extract_keywords(review_text)
        summary = summarize_text_using_title(review_title)
        time_taken = time.time() - start_time  # Time taken for the row

        logging.info(f"Row {review_id} processed in {time_taken:.2f} seconds.")
        return (review_id, sentiment_label, sentiment_score, keyword, summary, time_taken)

    except Exception as e:
        logging.error(f"Error during processing for review_id {review_id}: {e}")
        return None

# Process sentiment, keyword extraction, and summarization, and log to MLflow
def process_sentiment_analysis():
    mlflow.start_run(run_name="Optimized Sentiment Analysis with Keywords and Summarization")

    connection = get_oltp_connection()  # Connecting to OLTP for sentiment processing
    cursor = connection.cursor()

    # Log model info
    mlflow.log_param("model_name", "distilbert-base-uncased-finetuned-sst-2-english")
    mlflow.log_param("max_sequence_length", 512)

    # Fetch reviews
    cursor.execute("SELECT review_id, review_text, rating, review_title FROM Review WHERE sentiment_label IS NULL")
    reviews = cursor.fetchall()

    total_reviews = len(reviews)
    mlflow.log_metric("total_reviews_to_process", total_reviews)

    start_time = time.time()

    total_time = 0  # Track total processing time

    # Batch processing size
    BATCH_SIZE = 20  # Tune this value for optimal performance

    # Using ThreadPoolExecutor for concurrent execution
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(0, total_reviews, BATCH_SIZE):
            batch = reviews[i:i + BATCH_SIZE]
            future_to_review = {executor.submit(process_single_review, review): review for review in batch}
            
            for future in as_completed(future_to_review):
                result = future.result()
                if result:
                    review_id, sentiment_label, sentiment_score, keyword, summary, row_time = result
                    total_time += row_time
                    try:
                        # Update the Review table with the results
                        cursor.execute(
                            "UPDATE Review SET sentiment_label = ?, sentiment_score = ?, keyword = ?, sentiment_summary = ? WHERE review_id = ?",
                            (sentiment_label, sentiment_score, keyword, summary, review_id)
                        )
                        connection.commit()

                        # Log to MLflow
                        mlflow.log_metric("processed_review_id", review_id)
                        mlflow.log_metric("sentiment_score", sentiment_score)
                        mlflow.log_param(f"sentiment_label_review_{review_id}", sentiment_label)

                    except Exception as e:
                        logging.error(f"Error updating review_id {review_id}: {e}")

    cursor.close()
    connection.close()

    execution_time = time.time() - start_time
    avg_time_per_row = total_time / total_reviews if total_reviews > 0 else 0
    mlflow.log_metric("execution_time_in_seconds", execution_time)
    mlflow.log_metric("average_time_per_row", avg_time_per_row)
    logging.info(f"Processing completed in {execution_time:.2f} seconds. Average time per row: {avg_time_per_row:.2f} seconds.")

    mlflow.end_run()
