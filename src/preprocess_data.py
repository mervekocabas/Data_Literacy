# Import necessary libraries
import json
import csv
import requests
from bs4 import BeautifulSoup

# Get university keywords
def get_university_keywords():
    university_keywords = [
        "university", "college", "institute", "polytechnic", "department",
        "institut", "school", "iit", "academy", "eth", "epfl", "uc", "kaust", 
        "inria", "mit", "mpii saarland", "tu kaiserslautern",
        "dfki kaiserslautern", "upm", "mta sztaki", "cas", "caltech", 
        "cu boulder", "ctu", "école polytechnique fédérale de lausanne", 
        "école de technologie supérieure", "lausanne", "usc", "ut austin",
        "tu", "mpi", "kaist", "ku leuven", "hkust", "georgia tech", "gist",
        "universaity", "a&m", "cuhk", "postech", "cornell tech", "uestc",
        "technion", "univ", "umass", "unist", "unsv", "uestc", "vgg",
        "dlr", "riken", "a*star", "ihpc", "national", "fondazione bruno kessler",
        "cispa", "children’s hospital of philadelphia", "minds and machines",
        "ist austria", "paristech", "psl", "virginia tech", "nus", "iisc bangalore",
        "uts", "saarland informatics campus", "state key lab of intelligent technologies and systems",
        "zhejiang lab", "nyu", "bupt", "xjtlu", "ustb", "unsw", "iiai", "nasa", "fraunhofer itwm",
        "cea list", "lix", "rpi", "peng cheng laboratory", "computer vision center",
        "uenf", "memorial sloan kettering cancer center", "maple", "zhejiang provincial key",
        "multimedia group",
        "university", "college", "institute", "polytechnic", "department",
        "institut", "school", "iit", "academy", "eth", "epfl", "uc", "kaust", "inria", 
        "universität", "université", "universidade", "universidad", "università", "universiteit",
        "carnegie mellon", "universty", "univeristy", "universitat", "cornell tech", "ecole", "enpc",
        "ensta", "univrsity", "ctu", "cuhk", "cmu", "Caltech", "CentraleSupelec", "Georgia Tech",
        "hkbu", "hkust", "hnu", "hust", "Hochschule", "Universiry", "Universit", "Unviersity",
        "IBENS", "ICT", "Academia", "INSA", "Illinois Tech", "LMU", "MIT", "NTU", "Oxford", "Univerisity",
        "Politecnico", "Polytech", "SKKU", "SFU", "Stanford", "TU", "UBC", "Télécom Paris", "UESTC", "UMD",
        "UPenn", "USC", "UTokyo", "UW", "UW-Madison", "UZH", "UCL", "UvA", "Uviversité", "UW-Madison",
        "UMass", "UT Austin", "Virginia Tech", "Yale", "Universtiy", "École",
        "ANU", "Data61-CSIRO", "CIFAR AI Chair", "CSE, HBKU, Doha, Qatar", "Cornell", 
        "CryoEM Center, SUSTech", "Barcelona Supercomputing Center, Spain", 
        "Centre Borelli, ENS Paris-Saclay", "Data61-CSIRO", "Data61/CSIRO", 
        "Evelina London Children’s Hospital", "Fondazione Pascale", "Johns Hopkins Medicine", 
        "LIRIS, INSA - École Centrale, Lyon, UMR CNRS 5205, France", 
        "LIRIS, INSA-Lyon, UMR CNRS 5205, France", "Robarts Research, Canada", 
        "SIMTech, Agency for Science, Technology and Research", "SUNY Buffalo", 
        "UBC, Vancouver, Canada", "USTC", "UNC Chapel Hill", "VISTEC, Thailand", 
        "U.C. Santa Barbara", 
        "Australian Centre for Robotic Vision","Australian Centre of Excellence for Robotic Vision, Australia",
        "CMLA, ENS Cachan","CVC, UAB","Data61 CSIRO","Data61, CSIRO",
        "DFKI - German Research Center for Artificial Intelligence","ETS Montreal, Canada",
        "FORTH","KIST","LAAS-CNRS","LIGM, UPEM","Laboratory for Physical Sciences",
        "Laboratory for Physical Sciences, Booz Allen Hamilton, u.m.b.c.",
        "Laboratory for Physical Sciences, u.m.b.c.","MSRA","MUST, Macau, China",
        "NTT Media Intelligence Laboratories","NTT Service Evolution Laboratories",
        "PARC","Peng Cheng Laboratory, China", "Salesforce Research Asia, Singapore","Skoltech", "Cambridge",  "NTNU", "NSUT", "IISR Pune",
        "IMT Atlantique, Lab-STICC, team RAMBO, UMR CNRS 6285, F-29328, Brest, France", "ISI Kolkata", "SLU, Sweden",
        "TTI-Chicago", "AIIMS, New Delhi, India", "BITS Pilani", "CSIRO", "CHUV, Switzerland", "CERTH ITI, Greece", 
        "FAU Erlangen-Nürnberg, Erlangen, Germany", "ENS Paris-Saclay, Centre Borelli", "ETS Montreal", "ETS Montr´eal, Canada",
        "IISER", "IMSE-CNM", "KTH, Sweden", "CEDRIC (EA4329)", "BUET, Bangladesh", "KIT, Karlsruhe", "ISTI-CNR Pisa, Italy",
        "MBZUAI, UAE", "NIT Srinagar", "U. of Bern", "U. of Haifa", "UFMG, Brazil", "UNC Charlotte", "UQ, Australia", "UST, Republic of Korea",
        "UNC-Chapel Hill", "BUAA", "ECNU", "HKU", "Harvard", "KIT", "KULeuven", "Unversity", "Scuola Superiore", "Unibersity", "sysu", "AIIMS",
        "asu", "buaa", "hku", "iisc", "mila", "isti", "Northwestern", "shi", "USYD", "UT Dallas"
    ]
    return university_keywords

# Map of company names to their countries
company_country_map = {
    "Amazon Go": "USA",
    "Amazon Rekognition": "USA",
    "Amazon Web Services (AWS)": "USA",
    "Air Force Research Laboratory": "USA",
    "ASAPP Inc.": "USA",
    "Butterfly Network": "USA",
    "Facebook AI Research": "USA",
    "Facebook Reality Labs": "USA",
    "Google AI": "USA",
    "Google Brain": "USA",
    "Google Cloud": "USA",
    "Intel Labs": "USA",
    "Microsoft Research": "USA",
    "Microsoft Cloud & AI": "USA",
    "Microsoft": "USA",
    "OpenAI": "USA",
    "JD Digits": "USA",
    "Kwai Seattle AI Lab": "USA",
    "MarkableAI": "USA",
    "Magic Leap": "USA",
    "Megvii Research USA": "USA",
    "ByteDance AI Lab": "USA",
    "JD AI Research, Mountain View, USA": "USA",
    "AI Platform, Ytech Seattle AI Lab, FeDA Lab, Kwai Inc., Seattle, USA": "USA",
    "AI Labs, DiDi Chuxing": "USA",
    "Currently at Amazon AWS": "USA",
    "Dataminr Inc., New York, NY": "USA",
    "Facebook Reality Labs, Redmond, USA": "USA",
    "Facebook Reality Labs, Sausalito, USA": "USA",
    "Facebook Inc.": "USA",
    "Hewlett Packard Labs": "USA",
    "HRL Laboratories, LLC., Malibu, CA, USA": "USA",
    "IBM Research AI, Cambridge": "USA",
    "Interactive and Analytics Lab, Palo Alto Research Center, Palo Alto, CA": "USA",
    "Kitware Inc., Clifton Park, NY": "USA",
    "Mstar Technologies, Hangzhou, China": "USA",
    "Pinterest, USA": "USA",
    "Qualcomm AI Research": "USA",
    "Rimac Automobili, Sveta Nedelja, Croatia": "USA",
    "Scale AI": "USA",
    "Silicon Valley Research Center, JD.com, United States": "USA",
    "UNC-Charlotte, NC28223, USA": "USA",
    "X, The Moonshot Factory, Mountain View, USA": "USA",
    "AIoli Labs, USA": "USA",
    "Applied Research Center (ARC), Tencent PCG, USA": "USA",
    "Argo AI, USA": "USA",
    "Arm Inc., San Jose, CA, USA": "USA",
    "Bell Labs, NJ USA": "USA",
    "Cognitive Computing Lab, Baidu Research, Bellevue, USA": "USA",
    "Cloud+AI, Microsoft, United States": "USA",
    "JD Digits, Mountain View, CA, USA": "USA",
    "Kitware Inc., New York, USA": "USA",
    "Retrocausal, Inc., Seattle, WA": "USA",
    "Snap Inc., Santa Monica, CA": "USA",
    "Google Research, Perception Team": "USA",
    "Google Research, Brain Team": "USA",
    "Google Research, Mountain View, USA": "USA",
    "Google LLC": "USA",
    
    "Huawei Noah's Ark Lab": "China",
    "Alibaba Group": "China",
    "Baidu Inc.": "China",
    "ByteDance AI Lab": "China",
    "Tencent AI Lab": "China",
    "DJI": "China",
    "SenseTime": "China",
    "Horizon Robotics": "China",
    "Megvii (Face++)": "China",
    "Shenzhen Zhuke Innovation Technology": "China",
    "Shenzhen Malong AI Research Center": "China",
    "JD AI Research, Beijing, China": "China",
    "Alibaba Group, Hangzhou, China": "China",
    "Alibaba Inc.": "China",
    "Baidu Research(USA), 1195 Baudeaux Dr, Sunnyvale, CA, USA": "China",
    "Clova AI Research, NAVER Corp.": "China",
    "Huawei Technologies Co., Ltd.": "China",
    "Huawei Technologies Co., Ltd., China": "China",
    "Huawei Technologies, Beijing, China": "China",
    "Huawei Technologies, Zurich Research Center": "China",
    "Huawei Technologies, Shenzhen, China": "China",
    "Xiaomi AI Lab, Beijing, China": "China",
    "Xilinx Inc., Beijing, China": "China",
    "Megvii Research": "China",
    "JD AI Research, Beijing, China": "China",
    "Farsee2 Technology Ltd": "China",
    "ByteDance Intelligent Creation Lab": "China",
    "Huawei Cloud & AI": "China",
    "Huawei Inc.": "China",
    "Tencent Blade Team": "China",
    "Tencent Medical AI Lab, Beijing, China": "China",
    "Tencent Jarvis Lab, Shenzhen, China": "China",
    "Tencent PCG": "China",
    "Ping An Technology, Shenzhen, China": "China",
    "SenseTime Research, Shanghai AI Laboratory": "China",
    "Shanghai AI Laboratory": "China",
    "Shanghai Center for Brain Science and Brain-inspired Technology": "China",
    "Shanghai Em-Data Technology Co., Ltd.": "China",
    "Shenzhen People’s Hospital, China": "China",
    "Tetras.AI, Shanghai AI Laboratory": "China",
    "XForwardAI": "China",
    "Xilinx Inc., Beijing, China": "China",
    "ZhiJiang Laboratory": "China",
    
    "Anyvision Research Team, UK": "UK",
    "Tencent AI Lab, Seattle": "UK",
    "Samsung AI Center, Cambridge, UK": "UK",
    "FaceSoft.io, London, UK": "UK",
    "Yandex, Russia": "UK",
    "Zenith Ai, UK": "UK",
    "SLAMCore Ltd., UK": "UK",
    
    "Bosch Center for Artificial Intelligence (BCAI)": "Germany",
    "Siemens AG": "Germany",
    "Amazon, Tübingen": "Germany",
    "ADC Automotive Distance Control Systems GmbH, Continental, Germany": "Germany",
    "Spleenlab GmbH, Saalburg-Ebersdorf, Germany": "Germany",
    "Valeo Schalter und Sensoren GmbH, Kronach, Germany": "Germany",
    "Valeo.ai": "Germany",
    
    "Prophesee, Paris": "France",
    "Technicolor, Cesson Sévigné": "France",
    "Cerema, Équipe-projet STI, 10 rue Bernard Palissy, F-63017 Clermont-Ferrand, France": "France",
    "EDF R&D, Chatou, France": "France",
    "IDE MIA, France": "France",
    "Orange, Cesson-Sévigné, France": "France",
    
    "Lunit Inc.": "South Korea",
    "Samsung AI Center, Seoul": "South Korea",
    "A&B Center, LG Electronics, Seoul, South Korea": "South Korea",
    "Kakao Brain": "South Korea",
    "Kakao Corp.": "South Korea",
    "Kakao Enterprise": "South Korea",
    "Agency for Defense Development (ADD), Daejeon, Korea": "South Korea",
    "ETRI, South Korea": "South Korea",
    "SKT Vision AI Labs/T-Brain X, Seoul, Korea": "South Korea",
    "INEEJI, South Korea": "South Korea",
    "Naver Corporation, Korea": "South Korea",
    
    "NVIDIA, Tokyo, Japan": "Japan",
    "Sony Corporation, Tokyo": "Japan",
    "Panasonic Technology Division, Japan": "Japan",
    "NTT Communication Science Laboratories, NTT Corporation": "Japan",
    "AMD Japan Ltd": "Japan",
    
    "Horizon Robotics, Inc.": "Canada",
    "Huawei Technologies, Markham, ON": "Canada",
    "Laboratoire d’imagerie, ÉTS Montreal": "Canada",
    "Miovision Technologies Inc., Kitchener, Canada": "Canada",
    "Huawei Noah’s Ark Lab, Mila Montréal": "Canada",
    "Huawei Noah’s Ark Lab, INSA Lyon": "Canada",
    "Microsoft Research, Toronto, Canada": "Canada",
    "Vancouver General Hospital, Canada": "Canada",
    "Samsung AI Centre Toronto": "Canada",
    "Toronto AI Lab, LG Electronics Canada": "Canada",
    
    "MediaTek Inc., Hsinchu, Taiwan": "Taiwan",
    "ASUS Intelligent Cloud Services, Taiwan": "Taiwan",
    
    "PicsArt Inc.*, Moscow, Russian Federation": "Russia",
    "Yandex, Russia": "Russia",
    
    "Habana-Labs, Caesarea, Israel": "Israel",
    "Amazon Rekognition, Israel": "Israel",
    "Rafael - Advanced Defense Systems Ltd., Israel": "Israel",
    
    "Data61-CSIRO, Australia": "Australia",
    "FaceSoft.io, London, UK": "Australia",
    
    "NNAISENSE, Switzerland": "Switzerland",
    "Microsoft Research Artificial Intelligence and Mixed Reality Lab, Zürich, Switzerland": "Switzerland",
    
    "Wide-Eyes Technologies, Barcelona, Spain": "Spain",
    "Kognia Sports Intelligence, Spain": "Spain",
    
    "Rimac Automobili, Sveta Nedelja, Croatia": "Croatia",
    
    "Delta Research Center, Singapore": "Singapore",
    "Salesforce Research Asia, Singapore": "Singapore"
}

# Function to determine company country based on keywords in the affiliation
def get_company_country_from_keywords(affiliation):
    """
    Get the country for a given affiliation string based on company-related keywords.

    Args:
        affiliation (str): The affiliation string to check.

    Returns:
        str: The country of the company, or 'Unknown' if no match is found.
    """
    # Check if any known company keywords appear in the affiliation
    affiliation = affiliation.lower()  # Make it case-insensitive
    for company_name in company_country_map.keys():
        if company_name.lower() in affiliation:
            return company_country_map[company_name]  # Return the country if a match is found
    return "Unknown"  # Return "Unknown" if no match is found

# check the affiliations
def extract_affiliations(json_file_path):
    """
    Extract affiliations from a JSON dataset, filter by university keywords,
    and return unique non-university affiliations.

    Args:
        json_file_path (str): Path to the input JSON file.

    Returns:
        list: Unique non-university affiliations.
    """
    university_keywords = get_university_keywords()

    def is_university(affiliation):
        """Check if an affiliation contains university-related keywords."""
        return any(keyword.lower() in affiliation.lower() for keyword in university_keywords)

    # Load the JSON data
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    # Extract all affiliations
    all_affiliations = set()  # Use a set to store unique affiliations
    for entry in data:
        if "aff" in entry and entry["aff"]:
            affiliations = [aff.strip() for aff in entry["aff"].split(";") if aff.strip()]
            all_affiliations.update(affiliations)

    # Filter affiliations
    non_university_affiliations = [aff for aff in all_affiliations if not is_university(aff)]

    return sorted(non_university_affiliations)  # Return sorted unique non-university affiliations

# Function to determine if an affiliation is a university or a company
def is_university(affiliation):
    """
    Check if an affiliation contains keywords commonly associated with universities.

    Args:
        affiliation (str): The affiliation string to check.

    Returns:
        bool: True if the affiliation is likely a university, False otherwise.
    """
    university_keywords = get_university_keywords()

    for keyword in university_keywords:
        if keyword.lower() in affiliation.lower():
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
    substring = "cvpr2020"
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
        "company_country",
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

        # Only assign company country if company percentage is greater than 0
        if company_percentage != "" and company_percentage > 0: 
            # Extract company country based on keywords in the affiliation
            company_country = "Unknown"
            if "aff" in entry and entry["aff"]:
                affiliations = [aff.strip() for aff in entry["aff"].split(";") if aff.strip()]
                for aff in affiliations:
                    company_country = get_company_country_from_keywords(aff)
                    if company_country != "Unknown":  # Stop checking once a company is found
                        break
            entry["company_country"] = company_country  # Add the company country column

        # If company_percentage is 0, do not assign company_country
        else:
            entry["company_country"] = ""

        if "oa" in entry and entry["oa"]:
            entry["abstract"] = scrape_abstract(entry["oa"])
        elif "site" in entry and entry["site"]:
            entry["abstract"] = scrape_abstract(entry["site"])
        else:
            entry["abstract"] = ""

        filtered_entry = {key: entry.get(key, "") for key in headers}
        processed_data.append(filtered_entry)

    # Write the processed data to a CSV
    with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()  # Write the header row
        writer.writerows(processed_data)  # Write the data rows

    print(f"CSV file created successfully at {csv_file_path}")

# Main function to execute the script
def main():
    """
    Main function to process the dataset and output the CSV.
    """
    # Change the file paths only
    # If you want the affiliation txt close the process the dataset part
    json_file_path = "./Data_Literacy/cvpr/cvpr2022.json"
    csv_file_path = "wacv/wacv2020_with_affiliations.csv"
    check_affiliation_path = "./Data_Literacy/cvpr/non_university_affiliations_2022.txt"
    
    # Extract non-university affiliations
    non_university_affiliations = extract_affiliations(json_file_path)

    # Save results to a file
    with open(check_affiliation_path, "w", encoding="utf-8") as output_file:
        for aff in non_university_affiliations:
            output_file.write(f"{aff}\n")
        
    # Process the dataset
    #process_dataset(json_file_path, csv_file_path)

# Entry point of the script
if __name__ == "__main__":
    main()
