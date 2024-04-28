import re
import csv
import pandas as pd

class EmailExtractor:
    def __init__(self, filename):
        self.filename = filename
        self.existing_emails = []

    def extract_emails_from_file(self):
        try:
            # Read text from file with specified encoding (UTF-8)
            with open(self.filename, "r", encoding="utf-8") as file:
                text = file.read()
                # Extract email addresses, names, and links from the text
                emails, names, links = self.extract_info(text)
                # Save emails to file
                return self.save_emails_to_file(emails, names, links)
        except FileNotFoundError:
            print("File not found.")
            return []

    def extract_info(self, text):
        # Regular expression patterns
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        name_pattern = r"[\w\s]+ \([@\w\s]+\)"
        link_pattern = r"(?:http|ftp|https)://[\w_-]+(?:\.[\w_-]+)+"

        # Extract email addresses, names, and links from the text
        emails = re.findall(email_pattern, text)
        names = re.findall(name_pattern, text)
        links = re.findall(link_pattern, text)

        return emails, names, links

    def save_emails_to_file(self, emails, names, links):
        # Create a DataFrame to store the data
        data = {
            'Name': names,
            'Email': emails,
            'Link': links
        }
        df = pd.DataFrame(data)

        # Save DataFrame to Excel and CSV files
        excel_file = "emails_data.xlsx"
        csv_file = "emails_data.csv"

        df.to_excel(excel_file, index=False)
        df.to_csv(csv_file, index=False)

        return excel_file, csv_file
    

def scrape_and_extract_emails():
        print("Scraping...")

        print("Extracting emails...")
        email_extractor = EmailExtractor("scraped_content.txt")
        file_location_emails = email_extractor.extract_emails_from_file()
        print(f"Emails extracted and saved to: {file_location_emails}")
        
        print(file_location_emails)

scrape_and_extract_emails()