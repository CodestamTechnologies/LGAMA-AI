import argparse
import os
import subprocess
import sys
from google_scraper import run_google_scraper
from email_extractor import EmailExtractor

class EmailScraper:
    def __init__(self, query, max_scrolls=5):
        self.query = query
        self.max_scrolls = max_scrolls
    
    def scrape_and_extract_emails(self):
        print("\033[94mScraping...\033[0m")  
        file_location = run_google_scraper(self.query, self.max_scrolls)
        
        print("\033[94mExtracting emails...\033[0m") 
        email_extractor = EmailExtractor(file_location)
        file_location_emails = email_extractor.extract_emails_from_file()
        print(f"\033[92mEmails extracted and saved to: {file_location_emails}\033[0m") 
        
        return file_location_emails

class EmailSender:
    def __init__(self, file_location_emails):
        self.file_location_emails = file_location_emails
    
    def send_emails(self):
        print("\033[92mEmail extraction complete.\033[0m")
        os.chdir("mailer")
        subprocess.run(["node", "main.js", self.file_location_emails])
        os.chdir("..")

def main():
    if len(sys.argv) <= 1:
        print("\033[91mNo arguments found. Looking for queries.txt file for scraping.\033[0m") 
        query_file = "queries.txt"
        if not os.path.exists(query_file):
            print("\033[91mQuery file not found.\033[0m")  
            return
        
        with open(query_file, "r") as file:
            print("\033[94mFound queries.txt\033[0m")  
            queries = file.readlines()
            for query in queries:
                query = query.strip()
                if query and not query.startswith("#"):
                    scrape_and_send_emails(query)
    else:
        parser = argparse.ArgumentParser(description="Scrape Google for emails related to a query and send them via email.")
        parser.add_argument("query", help="Query to search on Google (enclose in quotes if it contains spaces)")
        args = parser.parse_args()
        scrape_and_send_emails(args.query)

def scrape_and_send_emails(query):
    if os.path.exists("Data/countries.txt"):
        with open("Data/countries.txt", "r") as states_file:
            states = states_file.readlines()
            for state in states:
                state = state.strip()
                if state:
                    query_input_file = "query_input.txt"
                    if not os.path.exists(query_input_file):
                        with open(query_input_file, "w") as file:
                            file.write(f'{query} ({state})' + "\n")
                    else:
                        with open(query_input_file, "a") as file:
                            file.write(f'{query} ({state})' + "\n")
                    print(f'\033[94mScraping for: {query} ({state})\033[0m') 
                    email_scraper = EmailScraper(query=f'{query} ({state})')
                    file_location_emails = email_scraper.scrape_and_extract_emails()
                    email_sender = EmailSender(file_location_emails)
                    email_sender.send_emails()

if __name__ == "__main__":
    main()
