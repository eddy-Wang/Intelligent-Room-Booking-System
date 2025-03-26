import os
import csv
import subprocess
import logging
import sys
import mysql.connector
from datetime import datetime
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("schedule_updater.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    "host": "diidrbs.mysql.polardb.rds.aliyuncs.com",
    "port": 3306,
    "user": "administrator",
    "password": "!admin123",
    "database": "diidrbs"
}

class ScheduleUpdater:
    def __init__(self, max_attempts=5):
        """Initialize the schedule updater with configuration."""
        self.csv_file = "./all_lessons.csv"
        self.max_attempts = max_attempts
        self.db_conn = None
        self.cursor = None
    
    def connect_to_db(self):
        """Establish connection to the database."""
        try:
            self.db_conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.db_conn.cursor()
            logger.info("Successfully connected to database")
            return True
        except mysql.connector.Error as err:
            logger.error(f"Failed to connect to database: {err}")
            return False
    
    def close_db_connection(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.db_conn:
            self.db_conn.close()
        logger.info("Database connection closed")
    
    def run_crawler(self):
        """Run the crawler script with multiple attempts on failure."""
        for attempt in range(1, self.max_attempts + 1):
            logger.info(f"Running crawler (attempt {attempt}/{self.max_attempts})")
            try:
                # Run the crawler script as a subprocess
                result = subprocess.run(["python", "./crawler/crawler.py"], check=True, capture_output=True, text=True)
                logger.info(f"Crawler completed successfully: {result.stdout}")
                return True
            except subprocess.CalledProcessError as e:
                logger.error(f"Crawler failed (attempt {attempt}): {e.stderr}")
                if attempt < self.max_attempts:
                    logger.info(f"Retrying in 10 seconds...")
                    time.sleep(10)  # Wait before retrying
                else:
                    logger.error("Maximum attempts reached. Crawler failed.")
                    return False
    
    def run_converter(self):
        """Run the converter script to process CSV files."""
        try:
            logger.info("Running converter script")
            result = subprocess.run(["python", "./crawler/converter.py"], check=True, capture_output=True, text=True)
            logger.info(f"Converter completed successfully: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Converter failed: {e.stderr}")
            return False
    
    def get_current_db_records(self):
        """Retrieve current records from the database."""
        try:
            select_sql = "SELECT room_id, date, time FROM lesson"
            self.cursor.execute(select_sql)
            records = {}
            
            for (room_id, date, time_slots) in self.cursor.fetchall():
                # Convert date to string format
                date_str = date.strftime("%Y-%m-%d") if isinstance(date, datetime) else str(date)
                key = (int(room_id), date_str)
                records[key] = time_slots
            
            logger.info(f"Retrieved {len(records)} records from database")
            return records
        except mysql.connector.Error as err:
            logger.error(f"Error retrieving records from database: {err}")
            return {}
    
    def read_csv_records(self):
        """Read records from the generated CSV file."""
        records = {}
        try:
            if not os.path.exists(self.csv_file):
                logger.error(f"CSV file not found: {self.csv_file}")
                return records
                
            with open(self.csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    room_id = int(row["room_id"])
                    date_str = row["date"]
                    time_slots = row["time"]
                    key = (room_id, date_str)
                    records[key] = time_slots
                    
            logger.info(f"Read {len(records)} records from CSV file")
            return records
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            return {}
    
    def compare_and_update_db(self, csv_records, db_records):
        """Compare CSV and DB records and update the database accordingly."""
        if not csv_records:
            logger.warning("No CSV records to process")
            return
            
        try:
            # Records to add (in CSV but not in DB)
            to_add = []
            for key, time_slots in csv_records.items():
                if key not in db_records:
                    to_add.append((key[0], key[1], time_slots))
            
            # Records to update (in both but with different time_slots)
            to_update = []
            for key, time_slots in csv_records.items():
                if key in db_records and db_records[key] != time_slots:
                    to_update.append((time_slots, key[0], key[1]))
            
            # Records to delete (in DB but not in CSV)
            to_delete = []
            for key in db_records:
                if key not in csv_records:
                    to_delete.append((key[0], key[1]))
            
            # Execute database operations
            if to_add:
                insert_sql = "INSERT INTO lesson (room_id, date, time) VALUES (%s, %s, %s)"
                self.cursor.executemany(insert_sql, to_add)
                logger.info(f"Added {len(to_add)} new records")
            
            if to_update:
                update_sql = "UPDATE lesson SET time = %s WHERE room_id = %s AND date = %s"
                self.cursor.executemany(update_sql, to_update)
                logger.info(f"Updated {len(to_update)} existing records")
            
            if to_delete:
                delete_sql = "DELETE FROM lesson WHERE room_id = %s AND date = %s"
                self.cursor.executemany(delete_sql, to_delete)
                logger.info(f"Deleted {len(to_delete)} obsolete records")
            
            # Commit changes
            self.db_conn.commit()
            logger.info(f"Database synchronization completed successfully")
        
        except mysql.connector.Error as err:
            logger.error(f"Database update error: {err}")
            self.db_conn.rollback()
    
    def run(self):
        """Run the complete update process."""
        try:
            # Step 1: Run crawler (with retry)
            if not self.run_crawler():
                logger.error("Crawler failed after maximum attempts. Aborting.")
                return False
            
            # Step 2: Run converter
            if not self.run_converter():
                logger.error("Converter failed. Aborting.")
                return False
            
            # Step 3: Connect to database
            if not self.connect_to_db():
                logger.error("Database connection failed. Aborting.")
                return False
            
            # Step 4: Get current database records
            db_records = self.get_current_db_records()
            
            # Step 5: Read new records from CSV
            csv_records = self.read_csv_records()
            
            # Step 6: Compare and update database
            self.compare_and_update_db(csv_records, db_records)
            
            logger.info("Schedule update process completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Unexpected error during update process: {e}")
            return False
            
        finally:
            # Always close database connection
            self.close_db_connection()

def main():
    """Main entry point for the schedule updater."""
    logger.info("Starting classroom schedule update process")
    updater = ScheduleUpdater()
    success = updater.run()
    
    if success:
        logger.info("Update process completed successfully")
        return 0
    else:
        logger.error("Update process failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())