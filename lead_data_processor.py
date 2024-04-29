import google.generativeai as genai
import time
import pandas as pd
import os

def retry(func):
    def wrapper(*args, **kwargs):
        retry_count = 0
        while retry_count < 3:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Error: {e}. Retrying...")
                time.sleep(2)
                retry_count += 1
        print(f"Failed to execute {func.__name__} after multiple retries.")
        return None
    return wrapper

class LeadDataProcessor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.model = None
        self.configure_generative_ai()

    def configure_generative_ai(self):
        genai.configure(api_key=self.api_key)
        generation_config = {"candidate_count": 1, "temperature": 1.0, "top_p": 0.7}
        safety_settings = [
            {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        self.model = genai.GenerativeModel(
            "gemini-pro", generation_config=generation_config, safety_settings=safety_settings
        )

    @retry
    def generate_content(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text

    def dataframe(self, lead_data):
        return pd.DataFrame([lead.split(',') for lead in lead_data.split('\n')])

    def save_to_excel(self, lead_data, filename):
        data = self.dataframe(lead_data)
        file_path = f"{filename}.xlsx"
        if os.path.exists(file_path):
            existing_data = pd.read_excel(file_path)
            updated_data = pd.concat([existing_data, data], ignore_index=True)
            updated_data.to_excel(file_path, index=False)
        else:
            data.to_excel(file_path, index=False)
        return file_path

    def save_to_csv(self, lead_data, filename):
        data = self.dataframe(lead_data)
        file_path = f"{filename}.csv"
        if os.path.exists(file_path):
            existing_data = pd.read_csv(file_path)
            # Check if any rows in the new data already exist in the existing data
            new_rows = data[~data.isin(existing_data)].dropna()
            if not new_rows.empty:
                updated_data = pd.concat([existing_data, new_rows], ignore_index=True)
                updated_data.to_csv(file_path, index=False)
        else:
            data.to_csv(file_path, index=False)
        return file_path


def process_lead_data(api_key, file_location):
    with open(file_location, 'r', encoding='utf-8') as file:
        data = file.read()

    processor = LeadDataProcessor(api_key)
    prompt = f"Form this {data} given above extract data in a csv format as name,emailid,social link, profession and only return the data in codeblock and no additional data" 
    lead_data = processor.generate_content(prompt=prompt)
    lead_data = lead_data.replace("`", "")
    lead_data = lead_data.replace("name,emailid,social link, profession", "")
    csv_file = processor.save_to_csv(lead_data, "lead_data")
    excel_file = processor.save_to_excel(lead_data, "lead_data")
    return csv_file, excel_file
