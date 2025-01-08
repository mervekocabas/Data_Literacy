from urllib.request import Request, urlopen  # Ensure this line is present
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
from bs4 import BeautifulSoup
import csv
import re
import json

# Initialize a persistent Chrome WebDriver
def initialize_driver():
    options = Options()
    options.add_experimental_option("detach", True)  # Keeps the browser open
    driver = webdriver.Chrome(options=options)  # Ensure you have the correct driver for Chrome
    return driver

def scrape_ieee_data(site_url):

    """
    Scrapes IEEE metadata from a given IEEE Xplore document URL.

    This function sends a request to the provided IEEE Xplore URL with a custom user-agent,
    parses the HTML response, and extracts metadata embedded in the page's JavaScript.
    The metadata includes IEEE Keywords, Index Terms, Author Keywords, abstract, and citation count.

    Args:
        site_url (str): The URL of the IEEE Xplore document to scrape.

    Returns:
        list: A list containing IEEE Keywords, Index Terms, Author Keywords, Citation Count, 
              and Abstract in that order. Each element is extracted from the metadata or 
              returned as None if not available.
    """

    headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    req = Request(site_url, headers=headers)
    response = urlopen(req, timeout=10)
    html_text = response.read()
    soup = BeautifulSoup(html_text, "html.parser")

    script_tags = soup.find('body').find_next('div', id='LayoutWrapper').find_all('script', type='text/javascript')
    
    for script in script_tags:
        if script.string and 'xplGlobal.document.metadata' in script.string:
            # Extract the metadata using regex
            metadata_match = re.search(r'xplGlobal\.document\.metadata\s*=\s*({.*?});', script.string, re.DOTALL)
            if metadata_match:
                metadata_json = json.loads(metadata_match.group(1))
                keywords = metadata_json.get('keywords', [])
                organized_keywords = {entry['type']: entry['kwd'] for entry in keywords}
                ieee_keywords = organized_keywords['IEEE Keywords'] if 'IEEE Keywords' in organized_keywords else None
                ieee_index_terms = organized_keywords['Index Terms'] if 'Index Terms' in organized_keywords else None
                ieee_author_keywords = organized_keywords['Author Keywords'] if 'Author Keywords' in organized_keywords else None
                ieee_abstract = metadata_json.get('abstract') if metadata_json.get('abstract') else None
                ieee_citations = int(metadata_json.get('citationCount')) if metadata_json.get('citationCount') else None
    return [ieee_keywords, ieee_index_terms, ieee_author_keywords, ieee_citations, ieee_abstract]

def get_ieee_link(paper_title, driver):
    """
    Scrape IEEE Xplore for the link to a specific paper.

    Args:
        paper_title (str): The title of the paper to search for.
        driver: The WebDriver instance to use.

    Returns:
        str: The URL of the paper on IEEE Xplore, or None if the link is not found.
    """
    encoded_title = urllib.parse.quote(paper_title)
    search_url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText={encoded_title}"
    
    driver.get(search_url)
    try:
        # Wait for search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "List-results-items"))
        )
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all <a> tags with class="fw-bold" in the search results
        search_results = soup.find_all("a", class_="fw-bold")
        for result in search_results:
            extracted_title = result.get_text()
            if extracted_title.lower() == paper_title.lower():  # Match the titles (case-insensitive)
                document_link = result['href']
                full_link = f"https://ieeexplore.ieee.org{document_link}"
                return full_link
    except Exception as e:
        print(f"Error while fetching link for {paper_title}: {e}")
    return None


def process_csv_and_update(input_csv, driver):
    """
    Process a CSV file and update it with IEEE Xplore data.

    Args:
        input_csv (str): The path to the CSV file to process.
        driver: The WebDriver instance to use.

    Returns:
        None
    """
    # Read the CSV into memory
    with open(input_csv, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)  # Load rows into memory
        fieldnames = reader.fieldnames

        # Check if the 'ieee_link', 'ieee_keywords', 'ieee_citations', and 'ieee_abstract' column exists, add it if not
        fields_to_add = ['ieee_link', 'ieee_keywords', 'ieee_index_terms', 'ieee_author_keywords', 'ieee_citations', 'ieee_abstract']        
        for field in fields_to_add:
            if field not in fieldnames:
                fieldnames.append(field)
                for row in rows:
                    row[field] = None
                 
    # Scrape IEEE links, keywords, citations, and abstract and update the rows
    for row in rows:
        title = row['title']
        if not row.get('ieee_link'):  # Skip if the link already exists
            print(f"Processing title: {title}")
            ieee_link = get_ieee_link(title, driver)
            if ieee_link:
                row['ieee_link'] = ieee_link
                print(f"Link for '{title}': {ieee_link}")
                ieee_keywords, ieee_index_terms, ieee_author_keywords, ieee_citations, ieee_abstract = scrape_ieee_data(ieee_link)
                row['ieee_keywords'] = ieee_keywords
                row['ieee_index_terms'] = ieee_index_terms
                row['ieee_author_keywords'] = ieee_author_keywords
                row['ieee_citations'] = ieee_citations
                row['ieee_abstract'] = ieee_abstract
            else:
                print(f"Link for '{title}' does not exist")
                row['ieee_link'] = None
                row['ieee_keywords'] = None
                row['ieee_index_terms'] = None
                row['ieee_author_keywords'] = None
                row['ieee_citations'] = None
                row['ieee_abstract'] = None        

    # Write back to the same CSV file
    with open(input_csv, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    driver = initialize_driver()  # Initialize the persistent browser
    input_csv = 'C:\\Users\\JAI GURU JI\\Desktop\\Data Lit\\Project\\Data_Literacy\\data\\cvpr_preprocessed\\cvpr2020.csv'  # Replace with your CSV file name
    process_csv_and_update(input_csv, driver)
