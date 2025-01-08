import pandas as pd
import pycountry
import re

data = pd.read_csv('/Users/irem/Desktop/Data_Literacy_Project/Data_Literacy/data/merged_dataset.csv')  # Replace with your file path

# Define country synonyms for standardization
country_synonyms = {
    "USA": "United States",
    "U.S.A.": "United States",
    "Mainland China": "China",
    "UK": "United Kingdom",
    "Usa": "United States",
    "Uk": "United Kingdom",
    "Uae": "United Arab Emirates",
    "China/France": "China, France",  # Choose one or split into separate entries if needed
    "Usa/India": "United States, India",  # Choose one
    "The Netherlands": "Netherlands",
    "Korea": "Korea, Republic of",  # Assume South Korea unless stated otherwise
    "Unknown": None,  # Remove unknown entries
    "Not Specified": None,  # Remove unspecified entries
    "South Korea": "Korea, Republic of",
    "Taiwan": "Taiwan, Province of China",
    "Viet Nam": "Vietnam",
    "Czechia": "Czech Republic",
    "Islamic Republic of Iran": "Iran",
    "Republic of Korea": "Korea, Republic of",
    "Province of China": "Taiwan",
    "Hong Kong": "Hong Kong",
    "Russia": "Russian Federation",
    "Macau": "Macao",
}

# Function to standardize a single country
def standardize_country_name(country):
    if pd.isna(country):
        return None
    country = country.strip().title()  # Normalize case
    if country in country_synonyms:
        return country_synonyms[country]
    try:
        return pycountry.countries.lookup(country).name
    except LookupError:
        return country  # Retain original if no match found
    
# Function to clean and standardize multiple countries in a single row
def standardize_countries(countries):
    if pd.isna(countries):
        return []
    # Split by commas, strip whitespace, and deduplicate
    country_list = list({standardize_country_name(c.strip()) for c in re.split(r'[,/]', countries)})
    return [c for c in country_list if c]  # Remove None or empty strings

# Apply the function to expand and standardize country names
data['university_country'] = data['university_country'].apply(standardize_countries)
data['company_country'] = data['company_country'].apply(standardize_countries)

print(len(data["company_country"]))
print(len(data["university_country"]))

# Write the updated data back to a CSV file
data.to_csv('/Users/irem/Desktop/Data_Literacy_Project/Data_Literacy/data/updated_dataset.csv', index=False)  # Replace with your file path
