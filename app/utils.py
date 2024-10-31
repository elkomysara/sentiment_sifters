# app/utils.py
def clean_reviewer_name(name):
    return name.strip().replace('"', '').replace("'", "''")  # Remove surrounding quotes and handle SQL single quotes

def generate_sentiment_analysis(review_text):
    """
    This function will perform sentiment analysis and keyword extraction.
    Replace this with actual sentiment analysis code using an ML model.
    """
    # Dummy sentiment analysis results for now
    sentiment_label = "Neutral"  # Could be Positive, Negative, Neutral
    sentiment_summary = "This is a summary of the sentiment."  # Summarize sentiment
    sentiment_score = 0.5  # Sentiment score, e.g., 0.5 for neutral
    keyword = "example_keyword"  # Extract keyword from the text
    return sentiment_label, sentiment_summary, sentiment_score, keyword

