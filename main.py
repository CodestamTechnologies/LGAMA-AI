import argparse
import os
import subprocess
import sys
from google_scraper import run_google_scraper
import lead_data_processor

class EmailScraper:
    def __init__(self, query, max_scrolls=5):
        self.query = query
        self.max_scrolls = max_scrolls
    
    def scrape_and_extract_emails(self, API_KEY):
        print("\033[94mScraping...\033[0m")  
        FILE_LOCATION = run_google_scraper(self.query, self.max_scrolls)
        
        print("\033[94mExtracting lead data...\033[0m") 
        
        result = lead_data_processor.process_lead_data(API_KEY, FILE_LOCATION)
        if result is None:
            print("Error: process_lead_data returned None")
            return
        csv_file, excel_file = result
        return csv_file, excel_file


def main(API_KEY):
    # Initialize EmailScraper with query and maximum scrolls
    query = '"instagram.com" "@gmail.com" "agency"'
    max_scrolls = 5
    scraper = EmailScraper(query, max_scrolls)
    
    # Call scrape_and_extract_emails method
    csv_file, excel_file = scraper.scrape_and_extract_emails(API_KEY)

    print(csv_file, excel_file)
    


if __name__ == "__main__":
    main("AIzaSyBPmSZH7N4LZvuRULlX12yd451IuccVBT0")
