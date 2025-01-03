# Import necessary libraries
import json
import csv
import requests
from bs4 import BeautifulSoup

# Function to determine if an affiliation is a university or a company
def is_university(affiliation):
    """
    Check if an affiliation contains keywords commonly associated with universities.

    Args:
        affiliation (str): The affiliation string to check.

    Returns:
        bool: True if the affiliation is likely a university, False otherwise.
    """
    university_keywords = [
        "university", "college", "institute", "polytechnic", "department", 
        "institut", "school", "iit", "academy", "eth", "epfl", "uc", "kaust", "inria"
    ]
    for keyword in university_keywords:
        if keyword in affiliation.lower():
            return True
    return False

# Function to process affiliations and calculate percentages
def calculate_affiliations_percentages(affiliation_string):
    """
    Calculate the percentage of university and company affiliations.

    Args:
        affiliation_string (str): The semicolon-separated string of affiliations.

    Returns:
        tuple: (university_percentage, company_percentage)
    """
    affiliations = [aff.strip() for aff in affiliation_string.split(";") if aff.strip()]
    university_count = sum(is_university(aff) for aff in affiliations)
    total_count = len(affiliations)
    if total_count == 0:
        return 0, 0
    university_percentage = (university_count / total_count) * 100
    company_percentage = 100 - university_percentage
    return university_percentage, company_percentage

# Function to check for a specific substring in a webpage (just for ECCV 2024)
def check_for_substring(url, substring):
    return substring in url.lower()

# Function to scrape the abstract from a given site URL
def scrape_abstract(site_url):
    """
    Scrape the abstract from a given site URL.

    Args:
        site_url (str): The URL of the site to scrape the abstract from.

    Returns:
        str: The abstract text if successfully scraped, otherwise an empty string.
    """
    substring = "eccv2024"
    try:
        response = requests.get(site_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            if check_for_substring(site_url, substring):
                abstract = soup.find('div', class_='collapse show', id='abstract_details').find('div', id='abstractExample').find('p')
            else:
                abstract = soup.find('div', id='content').find_next('div', id='abstract')  
        except:
            abstract = soup.find('div', class_='container papercontainer').find_next('div', id='content').find_next('div', id='abstract')  

        return abstract.text.strip() if abstract else ""

    except requests.RequestException as e:
        print(f"Error fetching abstract from {site_url}: {e}")
        return ""

# Function to process the dataset and write to a CSV
def process_dataset(json_file_path, csv_file_path):
    """
    Process a JSON dataset to calculate affiliation percentages and save it to a CSV.

    Args:
        json_file_path (str): Path to the input JSON file.
        csv_file_path (str): Path to the output CSV file.
    """
    # Load the JSON data
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    # Define the headers for the CSV
    headers = [
        "title",
        "author",
        "aff",
        "university_affiliation",
        "company_affiliation",
        "abstract",
        "site",
        "oa",
        "pdf",
        "project",
        "github",
        "arxiv",
        "track",
        "status"
    ]

    # Add new columns to the data
    processed_data = []
    for entry in data:
        if "aff" in entry and entry["aff"]:  # Check if 'aff' exists and is not empty
            university_percentage, company_percentage = calculate_affiliations_percentages(entry["aff"])
        else:
            university_percentage, company_percentage = "", ""  # Leave blank if 'aff' is missing or empty

        entry["university_affiliation"] = university_percentage
        entry["company_affiliation"] = company_percentage

        if "site" in entry and entry["site"]:
            entry["abstract"] = scrape_abstract(entry["site"])
        elif "oa" in entry and entry["oa"]:
            entry["abstract"] = scrape_abstract(entry["oa"])
        else:
            entry["abstract"] = ""

        filtered_entry = {key: entry.get(key, "") for key in headers}
        processed_data.append(filtered_entry)

    # Write the processed data to a CSV
    with open(csv_file_path, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()  # Write the header row
        writer.writerows(processed_data)  # Write the data rows

    print(f"CSV file created successfully at {csv_file_path}")

# Main function to execute the script
def main():
    """
    Main function to process the dataset and output the CSV.
    """
    # Input and output file paths
    json_file_path = "/home/stud125/project/Data_Literacy/eccv/eccv2024.json"
    csv_file_path = "/home/stud125/project/Data_Literacy/eccv/eccv2024_with_affiliations.csv"

    # Process the dataset
    process_dataset(json_file_path, csv_file_path)

# Entry point of the script
if __name__ == "__main__":
    main()
