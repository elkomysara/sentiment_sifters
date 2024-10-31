# app/data_processing.py
import os
import csv
from datetime import datetime
from app.db_connection import get_oltp_connection, get_olap_connection
from app.utils import clean_reviewer_name

def process_csv_files(folder_path):
    # Use the OLTP connection since we're dealing with the sentiment_sifters (OLTP) data
    connection = get_oltp_connection()  
    cursor = connection.cursor()

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            process_single_file(file_path, cursor)
    
    cursor.close()
    connection.close()

def process_single_file(file_path, cursor):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            reviewer_name = clean_reviewer_name(row['reviewer'])

            # Insert Product
            cursor.execute("EXEC sp_InsertProduct ?, ?, ?", 
                           row['asin'], row['product_name'], row['product_type'])
            product_id = cursor.execute("SELECT product_id FROM Product WHERE asin = ?", row['asin']).fetchone()[0]
            
            # Insert Reviewer
            cursor.execute("EXEC sp_InsertReviewer ?, ?, ?, ?", 
                           reviewer_name, row['reviewer_location'], row['country'], row['region'])
            
            reviewer_result = cursor.execute("SELECT reviewer_id FROM Reviewer WHERE LOWER(reviewer_name) = LOWER(?)", reviewer_name).fetchone()
            
            if not reviewer_result:
                print(f"Reviewer not found for {row['reviewer']}. Skipping this review.")
                continue
            
            reviewer_id = reviewer_result[0]  # Extract reviewer_id

            # Process helpful votes
            helpful_votes, total_votes = process_helpful_votes(row['helpful'])

            # Convert date
            review_date = datetime.strptime(row['date'], "%B %d, %Y").date()

            # Convert rating
            rating = process_rating(row['rating'])

            # Insert Review with empty sentiment and keyword fields for now
            cursor.execute(
                "EXEC sp_InsertReview ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?",
                row['asin'], product_id, reviewer_id, helpful_votes, total_votes, rating, row['title'],
                review_date, row['review_text'], None, None, None, None  # Empty sentiment and keyword fields
            )
            
            # Commit after each row
            cursor.connection.commit()

def process_helpful_votes(helpful_str):
    helpful_votes, total_votes = 0, 0
    if 'of' in helpful_str:
        helpful_votes = int(helpful_str.split(' of ')[0].strip())
        total_votes = int(helpful_str.split(' of ')[1].strip())
    return helpful_votes, total_votes

def process_rating(rating_str):
    try:
        return int(float(rating_str))  # Convert to float first, then to int
    except ValueError:
        return None  # Handle invalid ratings
