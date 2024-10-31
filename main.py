# main.py
import logging
from app.db_setup import create_database_if_not_exists, create_oltp_tables, create_olap_tables
from app.data_processing import process_csv_files
from app.sentiment_processing import process_sentiment_analysis
from app.ssis_execution import run_ssis_package


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    folder_path = r'D:\D1\Depi\new_project\Sentiment_Sifters\sentiment_sifters_project\data\processed'
    
    logging.info("Starting the ETL pipeline...")

    try:
        # Step 1: Create databases if they don't exist
        # create_database_if_not_exists('sentiment_sifters')
        # create_database_if_not_exists('sentiment_warehouse')
        
        # Step 2: Create tables for OLTP and OLAP
        #create_oltp_tables()
        create_olap_tables()

        # Step 3: Process CSV files (if you have implemented it)
        # process_csv_files(folder_path)
        # logging.info("CSV processing pipeline completed successfully.")
        
        # Step 4: Run sentiment analysis (if you have implemented it)
        # logging.info("Starting sentiment analysis...")
        # process_sentiment_analysis()
        # logging.info("Sentiment analysis completed successfully.")
        #Step5: Run the SSIS packages
        print("Starting SSIS packages...")
        run_ssis_package('OLTP_to_OLAP.dtsx')
        print("SSIS packages completed.")
        
    except Exception as e:
        logging.error(f"Error occurred during processing: {e}")
        raise

if __name__ == "__main__":
    main()
