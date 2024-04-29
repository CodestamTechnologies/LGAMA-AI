import os
from google_scraper import run_google_scraper
import lead_data_processor
import time
import threading
from tkinter import filedialog
from plyer import notification
import customtkinter as ctk
import pandas as pd
import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import filedialog
import csv

API_KEY = ""
stop_all_operations = False

class LGAMA(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.stop_flag = threading.Event()
        self.setup_ui()

    def setup_ui(self):
        self.geometry("500x500")
        self.title("LGAMA-AI")
        ctk.set_appearance_mode("system")
        self.configure(fg_color=('#d1dadb', '#262833'))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_window_close)

        self.tab = ctk.CTkTabview(master=self, fg_color=('#84b898', '#4b4c56'), width=400, height=600)
        self.tab.pack(padx=20, pady=20)

        self.tab.add("Dom")
        self.tab.add("Config")
        self.tab.add("Scraped Data") 

        dom_tab = self.tab.tab("Dom")
        config_tab = self.tab.tab("Config")
        scraped_data_tab = self.tab.tab("Scraped Data") 


        self.setup_dom_tab(dom_tab)
        self.setup_config_tab(config_tab)
        self.setup_scraped_data_tab(scraped_data_tab)


    def check_input_fields(self):
        # Check if the keyword box is empty
        keyword = self.keyword_box.get()
        if not keyword:
            notification_title = "Error"
            notification_message = "Please enter a query."
            notification.notify(
                title=notification_title,
                message=notification_message,
                app_icon=None,
                timeout=5
            )
            return False

        # Check if the API key box is empty
        api_key = self.gemini_api.get()
        if not api_key:
            notification_title = "Error"
            notification_message = "Please enter the Gemini API key."
            notification.notify(
                title=notification_title,
                message=notification_message,
                app_icon=None,
                timeout=5
            )
            return False

        return True

    def setup_dom_tab(self, tab):
        self.keyword_box = self.create_entry(tab, "Enter Query", 300, "transparent", ("#3a3d46", "#a6a7ac"),
                                             ("#3a3d46", "#a6a7ac"), 0.5, 0.15, "center")
        self.scrape_btn = self.create_button(tab, "Scrape", ("#e5ede8", "#e5ede8"), ("#84b898", "#84b898"),
                                              ("#1d1f2b"), 0.305, 0.25, "center", command=self.start_scraping)
        self.stop_scrape_btn = self.create_button(tab, "Stop", ("#e5ede8", "#e5ede8"), ("#84b898", "#84b898"),
                                                   ("#1d1f2b"), 0.685, 0.25, "center", command=self.stop_scraping)
        self.scraper_output = self.create_textbox(tab, 350, 200, ("#d1dadb", "#262833"), 0.5, 0.72, "center")

    def setup_config_tab(self, tab):
        self.gemini_api = self.create_entry(tab, "Gemini API Key", 300, "transparent", ("#3a3d46", "#a6a7ac"),
                                           ("#3a3d46", "#a6a7ac"), 0.5, 0.16, "center")
        self.save_btn = self.create_button(tab, "Save", ("#e5ede8", "#e5ede8"), ("#84b898", "#84b898"),
                                            ("#1d1f2b"), 0.5, 0.53, "center", command=self.save_config_settings)
        
    def setup_scraped_data_tab(self, tab):
        self.scraped_data_frame = ttk.Frame(tab)
        self.scraped_data_frame.pack(fill=tk.BOTH, expand=True)

        self.scraped_data_tree = ttk.Treeview(self.scraped_data_frame)
        self.scraped_data_tree.pack(fill=tk.BOTH, expand=True)

        # Add a scrollbar
        self.scraped_data_scroll = ttk.Scrollbar(self.scraped_data_frame, orient=tk.VERTICAL,
                                                  command=self.scraped_data_tree.yview)
        self.scraped_data_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.scraped_data_tree.configure(yscrollcommand=self.scraped_data_scroll.set)

        # Add button to load lead_data.csv
        self.load_csv_button = self.create_button(tab, "Load CSV", ("#e5ede8", "#e5ede8"), ("#84b898", "#84b898"),
                                                  ("#1d1f2b"), 0.5, 0.05, "center", command=self.load_csv_file)
        
    def load_csv_file(self):
        # Load lead_data.csv into the Treeview widget
        csv_file_path = "lead_data.csv"  # Assuming it's in the same directory
        if os.path.exists(csv_file_path):
            # Clear existing rows
            for child in self.scraped_data_tree.get_children():
                self.scraped_data_tree.delete(child)

            # Insert headers and data
            with open(csv_file_path, newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                headers = next(csv_reader)
                self.scraped_data_tree["columns"] = headers
                for header in headers:
                    self.scraped_data_tree.heading(header, text=header)

                # Calculate column widths based on content
                column_widths = {header: tk.font.Font().measure(header) for header in headers}
                for row in csv_reader:
                    for i, cell in enumerate(row):
                        width = tk.font.Font().measure(cell)
                        if width > column_widths[headers[i]]:
                            column_widths[headers[i]] = width

                # Insert data and set column widths
                for header, width in column_widths.items():
                    self.scraped_data_tree.column(header, width=width, minwidth=100, stretch=tk.YES)
                csvfile.seek(0)  # Reset file pointer to read data again
                next(csv_reader)  # Skip headers this time
                for row in csv_reader:
                    self.scraped_data_tree.insert("", "end", values=row)
        else:
            self.display_error("Error: lead_data.csv not found.")

    def load_file_dialog(self):
        # Open file dialog to browse and load files
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",
                                                filetypes=(("Text files", "*.txt"), ("CSV files", "*.csv"),
                                                           ("Excel files", "*.xlsx;*.xls")))
        if file_path:
            _, extension = os.path.splitext(file_path)
            try:
                if extension == ".txt":
                    with open(file_path, "r") as file:
                        content = file.read()
                elif extension in [".csv", ".xlsx", ".xls"]:
                    df = pd.read_excel(file_path) if extension == ".xlsx" else pd.read_csv(file_path)
                    content = df.to_string(index=False)
                else:
                    content = "Unsupported file format."
            except Exception as e:
                content = f"Error: {str(e)}"
            self.scraped_data_textbox.delete(1.0, "end")
            self.scraped_data_textbox.insert("end", content)


    def save_config_settings(self):
        global API_KEY
        API_KEY = self.gemini_api.get()
        notification_title = "Config Settings Saved"
        notification_message = "Your Config settings have been successfully saved."
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_icon=None,
            timeout=5
        )

    def create_entry(self, master, placeholder_text, width, fg_color, text_color, placeholder_text_color, relx, rely,
                     anchor):
        entry = ctk.CTkEntry(master=master, placeholder_text=placeholder_text, width=width,
                             fg_color=fg_color, text_color=text_color,
                             placeholder_text_color=placeholder_text_color)
        entry.place(relx=relx, rely=rely, anchor=anchor)
        return entry

    def create_textbox(self, master, width, height, fg_color, relx, rely, anchor):
        textbox = ctk.CTkTextbox(master=master, width=width, height=height, fg_color=fg_color)
        textbox.place(relx=relx, rely=rely, anchor=anchor)
        return textbox

    def create_button(self, master, text, fg_color, hover_color, text_color, relx, rely, anchor, command=None):
        button = ctk.CTkButton(master=master, text=text, fg_color=fg_color, hover_color=hover_color,
                               text_color=text_color, command=command)
        button.place(relx=relx, rely=rely, anchor=anchor)
        return button

    def on_window_close(self):
        self.stop_flag.set()
        self.destroy()

    def update_progress(self, message):
        self.scraper_output.insert("end", message + "\n")
        self.scraper_output.see("end")

    def start_scraping(self):
        if not self.check_input_fields():
            return

        global stop_all_operations
        stop_all_operations = False  # Reset stop flag

        try:
            self.scrape_btn.configure(state="disabled")
            self.stop_flag.clear()
            self.update_progress("Started Scraping")
            threading.Thread(target=lambda: main(self.keyword_box.get(), API_KEY=API_KEY)).start()

        except Exception as e:
            self.display_error(f"Error while starting scraping: {e}")

    def stop_scraping(self):
        global stop_all_operations
        stop_all_operations = True
        self.scraper_output.insert("end", "Stopping all operations...\n")
        self.stop_scrape_btn.configure(state="disabled")

def custom_print(message):
    app.update_progress(message)



class EmailScraper:
    def __init__(self, query, max_scrolls=5):
        self.query = query
        self.max_scrolls = max_scrolls
    
    def scrape_and_extract_emails(self, API_KEY):
        custom_print("Scraping...")  
        FILE_LOCATION = run_google_scraper(self.query, self.max_scrolls)
        
        custom_print("Extracting lead data...") 
        
        result = lead_data_processor.process_lead_data(API_KEY, FILE_LOCATION)
        if result is None:
            custom_print("Error: process_lead_data returned None")
            return
        csv_file, excel_file = result
        return csv_file, excel_file


def main(QUERY, API_KEY):
    # Initialize EmailScraper with query and maximum scrolls
    query = QUERY
    max_scrolls = 5
    scraper = EmailScraper(query, max_scrolls)
    
    # Call scrape_and_extract_emails method
    csv_file, excel_file = scraper.scrape_and_extract_emails(API_KEY)

    custom_print(f"CSV file is saved as {csv_file}")
    custom_print(f"Excel file is saved as {excel_file}")

    # Check stop flag periodically and stop scraping if set
    while not stop_all_operations:
        time.sleep(1)  # Adjust sleep duration as needed
        if stop_all_operations:
            custom_print("Scraping stopped by user.")
            break


if __name__ == "__main__":
    app = LGAMA()
    app.mainloop()
