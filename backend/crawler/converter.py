import os
import csv
import re
from datetime import date, timedelta
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Base date for the first Monday of the semester
BASE_DATE = date(2025, 2, 17)  # 2025/2/17 as the first Monday

def get_actual_date(week, day):
    """Calculate the actual date based on week number and day of week (1-7)."""
    # Adjust day offset (0 for Monday, 1 for Tuesday, etc.)
    day_offset = day - 1
    # Calculate days from semester start
    days_offset = (week - 1) * 7 + day_offset
    return BASE_DATE + timedelta(days=days_offset)

def transform_sections(sections):
    """
    Transform section numbers:
      1-4 => 0-3
      5-10 => +1 => 6-11
    Returns a string like "0,1" or "5,8,9"
    """
    transformed = []
    for s in sections:
        if 1 <= s <= 4:
            transformed.append(s - 1)
        elif 5 <= s <= 10:
            transformed.append(s + 1)
    
    if not transformed:
        return ""
    return ",".join(str(x) for x in sorted(transformed))

def get_room_id(room_number):
    """
    Map room numbers to room IDs:
    - 635 => 3
    - 101-108 => 4-11
    - 116-119 => 12-15
    """
    try:
        room_num = int(room_number)
        if room_num == 635:
            return 3
        elif 101 <= room_num <= 108:
            return 4 + (room_num - 101)
        elif 116 <= room_num <= 119:
            return 12 + (room_num - 116)
    except ValueError:
        pass
    
    return None

class CSVToDatabaseConverter:
    def __init__(self, csv_dir="classroom_schedules"):
        """Initialize the converter with directory for CSV files."""
        self.csv_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "classroom_schedules")
        # Dictionary to store unique (room_id, date) combinations and their sections
        self.data_dict = {}
    
    def parse_timeslot(self, timeslot):
        """
        Parse the timeslot string (e.g., "20304") into day and periods.
        
        Args:
            timeslot (str): Timeslot in format "DPPPP" where D is day of week and P are periods
            
        Returns:
            tuple: (day_of_week, list_of_periods)
        """
        try:
            # First digit is day of week (1-7)
            day_of_week = int(timeslot[0])
            
            # Check for 11-12 periods which should be ignored
            if "11" in timeslot[1:]:
                return day_of_week, []
            
            # Direct mapping for other common patterns
            periods = []
            
            if "01" in timeslot[1:]:
                periods.extend([1, 2])  # 01 means periods 1 and 2
            if "03" in timeslot[1:]:
                periods.extend([3, 4])  # 03 means periods 3 and 4            
            if "05" in timeslot[1:]:
                periods.extend([5, 6])  # 05 means periods 5 and 6            
            if "07" in timeslot[1:]:
                periods.extend([7, 8])  # 07 means periods 7 and 8            
            if "09" in timeslot[1:]:
                periods.extend([9, 10])  # 09 means periods 9 and 10
            
            return day_of_week, periods
            
        except (ValueError, IndexError) as e:
            logger.error(f"Failed to parse timeslot '{timeslot}': {e}")
            return None, []

    def parse_weeks(self, weeks_str):
        """
        Parse the weeks string (e.g., "1-16" or "1-3,5,7-16") into a list of week numbers.
        
        Args:
            weeks_str (str): String describing weeks
            
        Returns:
            list: List of week numbers
        """
        week_list = []
        if not weeks_str:
            logger.warning(f"Empty weeks string")
            return week_list
        
        # Split by comma
        week_segments = weeks_str.split(',')
        
        for segment in week_segments:
            segment = segment.strip()
            
            # Check if it's a range (e.g., "1-16")
            if '-' in segment:
                start, end = map(int, segment.split('-'))
                week_list.extend(range(start, end + 1))
            else:
                # Single week
                try:
                    week_list.append(int(segment))
                except ValueError:
                    logger.warning(f"Invalid week segment: {segment}")
        
        return week_list

    def apply_week_type_filter(self, weeks, week_type):
        """
        Apply week type filter (full, odd, even) to the list of weeks.
        
        Args:
            weeks (list): List of week numbers
            week_type (str): Week type - 'full', 'odd', or 'even'
            
        Returns:
            list: Filtered list of week numbers
        """
        if week_type == 'full':
            return weeks
        elif week_type == 'odd':
            return [w for w in weeks if w % 2 == 1]
        elif week_type == 'even':
            return [w for w in weeks if w % 2 == 0]
        else:
            logger.warning(f"Unknown week type: {week_type}, using 'full' as default")
            return weeks

    def process_csv_file(self, filename):
        """
        Process a single CSV file and add data to the data dictionary.
        
        Args:
            filename (str): Path to CSV file
        """
        # Extract room number from filename
        match = re.search(r'906_(.+)\.csv$', filename)
        if not match:
            logger.error(f"Could not extract room identifier from filename: {filename}")
            return
        
        raw_identifier = match.group(1)
    
        # If the last three digits are not numbers, map to 635, otherwise take the last three digits
        if raw_identifier[-3:].isdigit():
            room_number = raw_identifier[-3:]
        else:
            room_number = "635"    
        
        # Look up room_id from mapping
        room_id = get_room_id(room_number)
        if room_id is None:
            logger.error(f"Room number {room_number} not found in mapping")
            return
            
        logger.info(f"Processing CSV for room {room_number} (ID: {room_id})")
        
        try:
            with open(filename, 'r', encoding='utf-8', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    logger.debug(f"Processing row: {row}")
                    
                    # Verify location matches room number
                    location = row.get('location', '')
                    if location != room_number:
                        logger.warning(f"Location mismatch in {filename}: expected {room_number}, got {location}")
                    
                    # Parse timeslot
                    day_of_week, periods = self.parse_timeslot(row.get('time_slot', ''))
                    if not day_of_week or not periods:
                        logger.debug(f"Skipping row due to invalid timeslot: {row.get('time_slot', '')}")
                        continue
                    
                    # Parse weeks
                    weeks_str = row.get('weeks', '')
                    logger.debug(f"Processing weeks string: '{weeks_str}'")
                    weeks = self.parse_weeks(weeks_str)
                    if not weeks:
                        logger.debug(f"Skipping row due to empty weeks list from: '{weeks_str}'")
                        continue
                    
                    
                    # Get week type
                    week_type = row.get('week_type', 'full')
                    logger.debug(f"Week type: {week_type}, original weeks: {weeks}")
                    
                    # Apply week type filter
                    filtered_weeks = self.apply_week_type_filter(weeks, week_type)
                    logger.debug(f"After filter: {filtered_weeks}")

                    # Transform periods according to the mapping rule
                    transformed_periods = [int(p) for p in transform_sections(periods).split(',') if p]
                    if not transformed_periods:
                        logger.debug(f"Skipping row due to empty transformed periods from: {periods}")
                        continue
                    
                    # Add data to dictionary for each week
                    for week in filtered_weeks:
                        actual_date = get_actual_date(week, day_of_week)
                        key = (room_id, actual_date)
                        
                        if key in self.data_dict:
                            # Update existing sections
                            self.data_dict[key].update(transformed_periods)
                        else:
                            # Add new entry
                            self.data_dict[key] = set(transformed_periods)
        
        except Exception as e:
            logger.error(f"Error processing file {filename}: {e}")
            import traceback
            logger.error(traceback.format_exc())

    def process_all_files(self):
        """Process all CSV files in the specified directory."""
        # Check if directory exists
        if not os.path.exists(self.csv_dir):
            logger.error(f"Directory not found: {self.csv_dir}")
            return
        
        # Process each file
        for filename in os.listdir(self.csv_dir):
            if filename.endswith('.csv'):
                file_path = os.path.join(self.csv_dir, filename)
                self.process_csv_file(file_path)
        
        logger.info(f"Processed {len(self.data_dict)} unique (room_id, date) combinations")

    def save_to_csv(self, output_file="all_lessons.csv"):
        """
        Save processed data to CSV file in the required format.
        
        Args:
            output_file (str): Output file path
        """
        try:
            # Sort by date, then room_id
            sorted_items = sorted(self.data_dict.items(), key=lambda kv: (kv[0][1], kv[0][0]))
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['room_id', 'date', 'time'])
                
                for (room_id, date), sections in sorted_items:
                    # Sort sections
                    sorted_sections = sorted(sections)
                    time = ",".join(map(str, sorted_sections))
                    
                    # Format date as YYYY-MM-DD
                    date_str = date.isoformat()
                    
                    writer.writerow([room_id, date_str, time])
            
            logger.info(f"Saved {len(sorted_items)} records to {output_file}")
        except Exception as e:
            logger.error(f"Error saving to file {output_file}: {e}")

def main():
    # Initialize converter
    converter = CSVToDatabaseConverter(csv_dir=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "classroom_schedules"))
    
    # Process all files
    converter.process_all_files()
    
    # Save to CSV
    converter.save_to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_lessons.csv"))
    
    return 0

if __name__ == "__main__":
    main()