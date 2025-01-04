# Import necessary libraries
import json
import csv
import requests
from bs4 import BeautifulSoup

# Map of company names to their countries
company_country_map = {
    "USA": [
        "Amazon Go",
        "Amazon Rekognition",
        "Amazon Web Services (AWS)",
        "Air Force Research Laboratory",
        "ASAPP Inc.",
        "Butterfly Network",
        "Facebook AI Research",
        "Facebook Reality Labs",
        "Google AI",
        "Google Brain",
        "Google Cloud",
        "Intel Labs",
        "Microsoft Research",
        "Microsoft Cloud & AI",
        "Microsoft",
        "OpenAI",
        "JD Digits",
        "Kwai Seattle AI Lab",
        "MarkableAI",
        "Magic Leap",
        "Megvii Research USA",
        "ByteDance AI Lab",
        "JD AI Research, Mountain View, USA",
        "AI Platform, Ytech Seattle AI Lab, FeDA Lab, Kwai Inc., Seattle, USA",
        "AI Labs, DiDi Chuxing",
        "Currently at Amazon AWS",
        "Dataminr Inc., New York, NY",
        "Facebook Reality Labs, Redmond, USA",
        "Facebook Reality Labs, Sausalito, USA",
        "Facebook Inc.",
        "Hewlett Packard Labs",
        "HRL Laboratories, LLC., Malibu, CA, USA",
        "IBM Research AI, Cambridge",
        "Intel Labs",
        "Interactive and Analytics Lab, Palo Alto Research Center, Palo Alto, CA",
        "Kitware Inc., Clifton Park, NY",
        "Mstar Technologies, Hangzhou, China",
        "Pinterest, USA",
        "Qualcomm AI Research",
        "Rimac Automobili, Sveta Nedelja, Croatia",
        "Scale AI",
        "Silicon Valley Research Center, JD.com, United States",
        "UNC-Charlotte, NC28223, USA",
        "X, The Moonshot Factory, Mountain View, USA",
        "AIoli Labs, USA",
        "Applied Research Center (ARC), Tencent PCG, USA",
        "Argo AI, USA",
        "Arm Inc., San Jose, CA, USA",
        "Bell Labs, NJ USA",
        "Cognitive Computing Lab, Baidu Research, Bellevue, USA",
        "Cloud+AI, Microsoft, United States",
        "JD Digits, Mountain View, CA, USA",
        "Kitware Inc., New York, USA",
        "Retrocausal, Inc., Seattle, WA",
        "Snap Inc., Santa Monica, CA"
    ],
    "China": [
        "Huawei Noah's Ark Lab",
        "Alibaba Group",
        "Baidu Inc.",
        "ByteDance AI Lab",
        "Tencent AI Lab",
        "DJI",
        "SenseTime",
        "Horizon Robotics",
        "Megvii (Face++)",
        "Shenzhen Zhuke Innovation Technology",
        "Shenzhen Malong AI Research Center",
        "JD AI Research, Beijing, China",
        "Alibaba Group, Hangzhou, China",
        "Alibaba Inc.",
        "Baidu Research(USA), 1195 Baudeaux Dr, Sunnyvale, CA, USA",
        "Clova AI Research, NAVER Corp.",
        "Huawei Technologies Co., Ltd.",
        "Huawei Technologies Co., Ltd., China",
        "Huawei Technologies, Beijing, China",
        "Huawei Technologies, Zurich Research Center",
        "Huawei Technologies, Shenzhen, China",
        "Xiaomi AI Lab, Beijing, China",
        "Xilinx Inc., Beijing, China",
        "Megvii Research",
        "JD AI Research, Beijing, China",
        "Farsee2 Technology Ltd",
        "ByteDance Intelligent Creation Lab",
        "Huawei Cloud & AI",
        "Huawei Inc.",
        "Tencent Blade Team",
        "Tencent Medical AI Lab, Beijing, China",
        "Tencent Jarvis Lab, Shenzhen, China",
        "Tencent PCG",
        "Ping An Technology, Shenzhen, China",
        "SenseTime Research, Shanghai AI Laboratory",
        "Shanghai AI Laboratory",
        "Shanghai Center for Brain Science and Brain-inspired Technology",
        "Shanghai Em-Data Technology Co., Ltd.",
        "Shenzhen People’s Hospital, China",
        "Tetras.AI, Shanghai AI Laboratory",
        "XForwardAI",
        "Xilinx Inc., Beijing, China",
        "ZhiJiang Laboratory"
    ],
    "UK": [
        "Anyvision Research Team, UK",
        "Tencent AI Lab, Seattle",
        "Samsung AI Center, Cambridge, UK",
        "FaceSoft.io, London, UK",
        "Yandex, Russia",
        "Zenith Ai, UK",
        "SLAMCore Ltd., UK"
    ],
    "Germany": [
        "Bosch Center for Artificial Intelligence (BCAI)",
        "Siemens AG",
        "Amazon, Tübingen",
        "ADC Automotive Distance Control Systems GmbH, Continental, Germany",
        "Google Research, Perception Team",
        "Google Research, Brain Team",
        "Google Research, Mountain View, USA",
        "Google LLC",
        "Spleenlab GmbH, Saalburg-Ebersdorf, Germany",
        "Valeo Schalter und Sensoren GmbH, Kronach, Germany",
        "Valeo.ai"
    ],
    "France": [
        "Prophesee, Paris",
        "Technicolor, Cesson Sévigné",
        "Cerema, Équipe-projet STI, 10 rue Bernard Palissy, F-63017 Clermont-Ferrand, France",
        "EDF R&D, Chatou, France",
        "IDE MIA, France",
        "Orange, Cesson-Sévigné, France"
    ],
    "South Korea": [
        "Lunit Inc.",
        "Samsung AI Center, Seoul",
        "A&B Center, LG Electronics, Seoul, South Korea",
        "Kakao Brain",
        "Kakao Corp.",
        "Kakao Enterprise",
        "Agency for Defense Development (ADD), Daejeon, Korea",
        "ETRI, South Korea",
        "SKT Vision AI Labs/T-Brain X, Seoul, Korea",
        "INEEJI, South Korea",
        "Naver Corporation, Korea"
    ],
    "Japan": [
        "NVIDIA, Tokyo, Japan",
        "Sony Corporation, Tokyo",
        "Panasonic Technology Division, Japan",
        "NTT Communication Science Laboratories, NTT Corporation"
    ],
    "Canada": [
        "Horizon Robotics, Inc.",
        "Huawei Technologies, Markham, ON",
        "Laboratoire d’imagerie, ÉTS Montreal",
        "Miovision Technologies Inc., Kitchener, Canada",
        "Huawei Noah’s Ark Lab, Mila Montréal",
        "Huawei Noah’s Ark Lab, INSA Lyon",
        "Microsoft Research, Toronto, Canada",
        "Vancouver General Hospital, Canada",
        "Samsung AI Centre Toronto",
        "Toronto AI Lab, LG Electronics Canada"
    ],
    "Taiwan": [
        "MediaTek Inc., Hsinchu, Taiwan",
        "ASUS Intelligent Cloud Services, Taiwan"
    ],
    "Russia": [
        "PicsArt Inc.*, Moscow, Russian Federation",
        "Yandex, Russia"
    ],
    "Israel": [
        "Habana-Labs, Caesarea, Israel",
        "Amazon Rekognition, Israel",
        "Rafael - Advanced Defense Systems Ltd., Israel"
    ],
    "Australia": [
        "Data61-CSIRO, Australia",
        "FaceSoft.io, London, UK"
    ],
    "Switzerland": [
        "NNAISENSE, Switzerland",
        "Microsoft Research Artificial Intelligence and Mixed Reality Lab, Zürich, Switzerland"
    ],
    "Spain": [
        "Wide-Eyes Technologies, Barcelona, Spain",
        "Kognia Sports Intelligence, Spain"
    ],
    "Croatia": [
        "Rimac Automobili, Sveta Nedelja, Croatia"
    ],
    "Singapore": [
        "Delta Research Center, Singapore",
        "Salesforce Research Asia, Singapore"
    ]
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
        "PARC","Peng Cheng Laboratory, China", "Salesforce Research Asia, Singapore","Skoltech"
    ]

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
        "PARC","Peng Cheng Laboratory, China", "Salesforce Research Asia, Singapore","Skoltech"
    ]

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
    # Change the file paths only
    # If you want the affiliation txt close the process the dataset part
    json_file_path = "/home/stud125/project/Data_Literacy/cvpr/cvpr2023.json"
    csv_file_path = "/home/stud125/project/Data_Literacy/cvpr/cvpr2023_with_affiliations.csv"
    check_affiliation_path = "/home/stud125/project/Data_Literacy/cvpr/non_university_affiliations_2023.txt"
    
    # Extract non-university affiliations
    non_university_affiliations = extract_affiliations(json_file_path)

    # Save results to a file
    with open(check_affiliation_path, "w", encoding="utf-8") as output_file:
        for aff in non_university_affiliations:
            output_file.write(f"{aff}\n")
        
    # Process the dataset
    process_dataset(json_file_path, csv_file_path)

# Entry point of the script
if __name__ == "__main__":
    main()
