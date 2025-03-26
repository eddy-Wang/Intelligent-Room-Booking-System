from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import os
import sys
import logging
import csv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ClassroomScheduleScraper:
    def __init__(self, username, password):
        """Initialize the scraper with login credentials"""
        self.username = username
        self.password = password
        
        # Chrome options setup
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Create output directory
        self.output_dir = "classroom_schedules"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def login(self):
        """Login to CSU portal"""
        try:
            logger.info("Opening login page...")
            self.driver.get("https://my.csu.edu.cn/")

            # Wait for username field to load
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

            # Enter credentials
            logger.info("Entering login credentials...")
            self.driver.find_element(By.ID, "username").send_keys(self.username)
            self.driver.find_element(By.ID, "password").send_keys(self.password)
            self.driver.find_element(By.ID, "login_submit").click()

            # Wait for login to complete
            logger.info("Waiting for login to complete...")
            time.sleep(5)

            # Click on undergraduate academic affairs button
            logger.info("Clicking on undergraduate academic affairs button...")
            bkjjw_item = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@title='本科生教务']"))
            )
            bkjjw_item.click()

            # Switch to new window if opened
            time.sleep(2)
            if len(self.driver.window_handles) > 1:
                logger.info("Switching to academic system window...")
                self.driver.switch_to.window(self.driver.window_handles[-1])
                
        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise

    def navigate_to_classroom_schedule(self):
        """Navigate to classroom schedule query page"""
        try:
            logger.info("Navigating to classroom schedule query page...")
            self.driver.get("http://csujwc.its.csu.edu.cn/tkglAction.do?method=tzkb&first=yes&type=1&isview=1&findType=cx")
            time.sleep(2)
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            raise

    def switch_to_iframe(self):
        """Switch to the main iframe where the form is located"""
        try:
            # Switch to the main form iframe
            iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ftop1"))
            )
            self.driver.switch_to.frame(iframe)
            logger.info("Successfully switched to the main iframe")
            return True
        except Exception as e:
            logger.error(f"Failed to switch to iframe: {e}")
            raise

    def select_classroom(self, building_id, classroom_id):
        """Select a specific classroom from the form and scrape its schedule"""
        try:
            # Select building (jzwid)
            building_select = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "jzwid"))
            )
            Select(building_select).select_by_value(building_id)
            logger.info(f"Selected building with ID: {building_id}")
            time.sleep(1)
            
            # Wait for classroom options to load
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "classroomID"))
            )
            
            # Select classroom
            classroom_select = self.driver.find_element(By.ID, "classroomID")
            Select(classroom_select).select_by_value(classroom_id)
            logger.info(f"Selected classroom with ID: {classroom_id}")
            time.sleep(1)
            
            # Click the search button
            search_button = self.driver.find_element(By.NAME, "CmdOK")
            search_button.click()
            logger.info("Clicked search button")
            
            # Wait for results to load
            time.sleep(3)
            
            # Call function to scrape schedule
            self.scrape_schedule(building_id, classroom_id)
            
        except Exception as e:
            logger.error(f"Error selecting classroom: {e}")
            raise

    def scrape_schedule(self, building_id, classroom_id):
        """Scrape classroom schedule data, including all pagination content"""
        try:
            # Create output directory if not exists
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
                
            # Create filename for this classroom's schedule
            classroom_filename = f"{self.output_dir}/{building_id}_{classroom_id}.csv"
            
            # Switch to results iframe
            results_iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "fbuttom"))
            )
            self.driver.switch_to.frame(results_iframe)
            logger.info(f"Scraping schedule for classroom {classroom_id} in building {building_id}")
            
            # Find data table and initialize a list to store all page data
            all_rows_data = []
            
            # Find total pages
            try:
                pagination_text = self.driver.find_element(By.XPATH, "//td[contains(text(), '页[')]").text
                total_pages = int(pagination_text.split('/')[1].split('页')[0])
                logger.info(f"Total pages: {total_pages}")
            except Exception as e:
                logger.warning(f"Could not determine total pages: {e}")
                total_pages = 1  # Default to at least one page
            
            # Process all pages
            current_page = 1
            while current_page <= total_pages:
                logger.info(f"Processing page {current_page}/{total_pages}")
                
                # Find data table and rows
                try:
                    table = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.ID, "dataTables"))
                    )
                    rows = table.find_elements(By.XPATH, ".//tbody/tr")
                    
                    if len(rows) == 0:
                        logger.info(f"No course data found on page {current_page}")
                    else:
                        logger.info(f"Found {len(rows)} course records on page {current_page}")
                        
                        # Process each row on current page
                        for row in rows:
                            # Get all cells in the row
                            cells = row.find_elements(By.TAG_NAME, "td")
                            
                            if len(cells) >= 13:  # Ensure row has enough cells
                                # Process room location, keep only room number (digits)
                                location_text = cells[8].text.strip()
                                # Extract numeric part (assuming room number is at the end)
                                room_number = ''.join(filter(str.isdigit, location_text))
                                
                                # Process week type conversion
                                week_type_text = cells[10].text.strip()
                                if '全周' in week_type_text:
                                    week_type = 'full'
                                elif '单周' in week_type_text:
                                    week_type = 'odd'
                                elif '双周' in week_type_text:
                                    week_type = 'even'
                                else:
                                    week_type = week_type_text  # Keep original value
                                
                                # Extract cell data
                                row_data = {
                                    'time_slot': cells[7].text.strip().replace(',', ''),  # Time slot
                                    'location': room_number,  # Room number only
                                    'weeks': cells[9].text.strip(),  # Weeks
                                    'week_type': week_type  # Converted week type
                                }
                                all_rows_data.append(row_data)
                
                except Exception as e:
                    logger.error(f"Error processing page {current_page}: {e}")
                    raise
                
                # If there's a next page, click the "next page" button
                if current_page < total_pages:
                    try:
                        next_button = self.driver.find_element(By.ID, "tablePagination_nextPage")
                        next_button.click()
                        logger.info(f"Clicked next page button, going to page {current_page + 1}")
                        
                        # Wait for page to load
                        time.sleep(2)
                        
                        # Confirm page has changed
                        WebDriverWait(self.driver, 10).until(
                            lambda d: d.find_element(By.XPATH, "//td[contains(text(), '页[')]").text.startswith(f"{current_page + 1}/")
                        )
                    except Exception as e:
                        logger.error(f"Error during pagination: {e}")
                        raise
                
                current_page += 1
            
            # Write all collected data to CSV file
            if len(all_rows_data) > 0:
                logger.info(f"Collected {len(all_rows_data)} course records total")
                

                with open(classroom_filename, 'w', encoding='utf-8', newline='') as f:
                    # Use the csv module's writer to properly handle commas in fields
                    writer = csv.DictWriter(f, fieldnames=['time_slot', 'location', 'weeks', 'week_type'])
                    writer.writeheader()
                    writer.writerows(all_rows_data)
                
                logger.info(f"Successfully saved all course data to {classroom_filename}")
            else:
                logger.info(f"No course data found")
                
                # Save empty data file
                with open(classroom_filename, 'w', encoding='utf-8') as f:
                    f.write("classroom_id,building_id,no_data\n")
                    f.write(f"{classroom_id},{building_id},no_course_data\n")
            
            # Switch back to main content
            self.driver.switch_to.default_content()
            
            # Switch back to form iframe
            self.switch_to_iframe()
            
        except Exception as e:
            logger.error(f"Error scraping schedule: {e}")
            # Attempt to recover to form state
            self.driver.switch_to.default_content()
            try:
                self.switch_to_iframe()
            except:
                pass
            raise

    def run(self, building_id, classroom_ids):
        """Run the scraper for multiple classrooms"""
        try:
            # Login to the system
            self.login()
            
            # Navigate to classroom schedule page
            self.navigate_to_classroom_schedule()
            
            # Switch to the iframe containing the form
            self.switch_to_iframe()
            
            # Process each classroom
            for classroom_id in classroom_ids:
                try:
                    self.select_classroom(building_id, classroom_id)
                    time.sleep(2)  # Brief pause between requests
                except Exception as e:
                    logger.error(f"Failed to process classroom {classroom_id}: {e}")
                    # Continue with next classroom
                    self.driver.switch_to.default_content()
                    self.switch_to_iframe()
            
            logger.info("All classrooms have been processed")
            
        except Exception as e:
            logger.error(f"An error occurred during execution: {e}")
            raise
        
        finally:
            logger.info("Script execution completed")
            self.driver.quit()


def main():
    """Main function to run the scraper"""
    try:
        # Login credentials
        USERNAME = "ADD_YOUR_CSU_ID_HERE"  # Replace with your CSU student ID
        PASSWORD = "ADD_YOUR_CSU_PASSWORD_HERE"  # Replace with your CSU password
        
        # Initialize and run scraper
        scraper = ClassroomScheduleScraper(USERNAME, PASSWORD)
        
        # Foreign Language Network Building ID
        building_id = "906"
        
        # List of classroom IDs to scrape
        classroom_ids = [
            "9060101",  # Foreign Language Network Building 101
            "9060102",  # Foreign Language Network Building 102
            "9060103",  # Foreign Language Network Building 103
            "9060104",  # Foreign Language Network Building 104
            "9060105",  # Foreign Language Network Building 105
            "9060106",  # Foreign Language Network Building 106
            "9060107",  # Foreign Language Network Building 107
            "9060108",  # Foreign Language Network Building 108
            "9060116",  # Foreign Language Network Building 116
            "9060117",  # Foreign Language Network Building 117
            "9060118",  # Foreign Language Network Building 118
            "9060119",  # Foreign Language Network Building 119
            "FD014E6967DD43C3AD07F6FA695327D1"  # Foreign Language Network Building 635
        ]
        
        # Run the scraper
        scraper.run(building_id, classroom_ids)
        
        return 0  # Successful execution
        
    except Exception as e:
        logger.critical(f"Critical error in main function: {e}")
        return 1  # Failed execution


if __name__ == "__main__":
    sys.exit(main())