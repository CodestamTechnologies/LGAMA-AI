import re

class EmailExtractor:
    def __init__(self, filename):
        self.filename = filename
        self.existing_emails = set()

    def extract_emails_from_file(self):
        try:
            print("\033[94mLoading existing emails...\033[0m")  # Blue color
            # Load existing emails from file
            self.load_existing_emails()
            print("\033[94mExisting emails loaded successfully.\033[0m")  # Blue color
            
            print("\033[94mExtracting emails from file...\033[0m")  # Blue color
            # Read text from file with specified encoding (UTF-8)
            with open(self.filename, "r", encoding="utf-8") as file:
                text = file.read()
                # Extract email addresses from the text
                emails = self.extract_emails(text)
                print(f"\033[94m{len(emails)} emails extracted successfully.\033[0m")  # Blue color
                
                # Filter out existing emails
                new_emails = [email for email in emails if email not in self.existing_emails]
                print(f"\033[94m{len(new_emails)} new emails found.\033[0m")  # Blue color
                
                # Save new emails to file
                return self.save_emails_to_file(new_emails)
        except FileNotFoundError:
            print("\033[91mFile not found.\033[0m")  # Red color
            return []

    def extract_emails(self, text):
        # Regular expression pattern to match email addresses
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        # Using re.findall to extract all email addresses from the text
        emails = re.findall(email_pattern, text)
        return emails

    def save_emails_to_file(self, emails):
        file_location = "extracted_emails.txt"
        print("\033[94mSaving new emails to file...\033[0m")  # Blue color
        # Write new emails to file, overwriting existing content
        with open(file_location, "w", encoding="utf-8") as file:
            # Write each new email to the file
            for email in emails:
                file.write(email + "\n")
            print("\033[94mNew emails saved successfully.\033[0m")  # Blue color
        
        # Add new emails to existing emails file
        all_mails_location = "all_mails.txt"
        with open(all_mails_location, "a+", encoding="utf-8") as all_mails_file:
            all_mails_file.seek(0)
            existing_emails = all_mails_file.read().splitlines()
            for email in emails:
                if email not in existing_emails:
                    all_mails_file.write(email + "\n")
                    print(f"\033[92mAdded new email: {email}\033[0m")  # Green color

        return file_location

    def load_existing_emails(self):
        try:
            all_mails_location = "all_mails.txt"
            # Read existing emails from file
            with open(all_mails_location, "r", encoding="utf-8") as file:
                self.existing_emails = set(file.read().splitlines())
        except FileNotFoundError:
            print("\033[91mExisting emails file not found. Creating a new one.\033[0m")  # Red color

            # Create a new file if it doesn't exist
            with open(all_mails_location, "w", encoding="utf-8") as file:
                pass  # Empty file

        return
