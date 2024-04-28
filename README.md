
# LGAMA: Lead Generation And Mailing Automation

LGAMA is an automation project developed in Python for lead generation and mailing tasks. It allows users to scrape Google for emails related to specified queries, extract relevant data, and send messages to collected contact details via email.

## Features

- **Google Search Automation**: LGAMA automates Google searches based on specified queries.
- **Data Extraction**: It extracts relevant data from the search results, including email addresses.
- **Contact Details Collection**: LGAMA collects email addresses and other contact details from the extracted data.
- **Email Sending Automation**: It provides functionality to send messages to the collected email addresses via email.
- **Batch Processing**: Users can process multiple queries in a batch using a text file.

```markdown
## Installation

1. Clone the repository:

```bash
git clone https://github.com/EnriqueStrange/LGAMA.git
```

2. Navigate to the project directory:

```bash
cd LGAMA
```

3. Install dependencies:

```bash
cd Mailer
npm install nodemailer dotenv
cd ..
pip install -r requirements.txt
```

4. Ensure you have Python installed on your system.

## Usage

### Scraping Google for Emails

#### Single Query

To scrape Google for emails related to a single query, run the following command:

```bash
python main.py "your_query_here"
```

Replace `"your_query_here"` with your desired query. Enclose the query in quotes if it contains spaces.

#### Batch Processing

To process multiple queries stored in a text file named `queries.txt`, run the following command:

```bash
python main.py
```

If `queries.txt` is found, LGAMA will iterate through each query in the file and perform scraping and emailing tasks for each query.

### Providing Queries via Command Line Arguments

You can also provide queries directly via command line arguments. For example:

```bash
python main.py '"query1" "query2" "query3"'
```

### Providing Queries via Text File

Create a text file named `queries.txt` in the project directory and add each query on a separate line. LGAMA will automatically detect and process queries from this file.

### Configuration

Ensure that you have configured the SMTP server details in a `.env` file with the following format:

```
SMTP_USERNAME=your_smtp_username
SMTP_PASSWORD=your_smtp_password
```

Replace `your_smtp_username` and `your_smtp_password` with your SMTP server credentials.

## Dependencies

- **argparse**: LGAMA uses the `argparse` module to handle command line arguments.
- **google_scraper**: This module is used for scraping Google search results.
- **email_extractor**: LGAMA relies on this module to extract email addresses from the scraped content.
- **subprocess**: It is used to run external commands like sending emails via Node.js scripts.
- **dotenv**: LGAMA utilizes the `dotenv` module to load environment variables from a `.env` file.

## Contributing

Contributions are welcome! If you'd like to contribute to LGAMA, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Credits

LGAMA was created by [Your Name].

## Support

For any questions or issues, please [open an issue](https://github.com/YourUsername/LGAMA/issues) on GitHub.

## Workflow

LGAMA's workflow can be visualized as follows:

```
+----------------+       +-------------------+       +------------------+
| Google Search  |  ==>  | Data Extraction   |  ==>  | Email Sending    |
| Automation     |       |                   |       | Automation       |
+----------------+       +-------------------+       +------------------+
        |                        |                          |
        |                        |                          |
        +------------------------+--------------------------+
                                 |
                                 v
                          +--------------+
                          | Batch        |
                          | Processing   |
                          +--------------+
```

LGAMA automates the process of searching Google for relevant data, extracting email addresses and other contact details, and sending emails to the collected addresses. It also supports batch processing of multiple queries stored in a text file.
