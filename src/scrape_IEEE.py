from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json
import csv
import re


def extract_metadata_json(site_url, json_name):
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
                metadata_json = json.loads(metadata_match.group(1))  # Parse as JSON
                with open(json_name, 'w', encoding='utf-8') as file:
                    json.dump(metadata_json, file, indent=4, ensure_ascii=False)
    return None


def main():
    site_url = 'https://ieeexplore.ieee.org/document/10204476'
    extract_metadata_json(site_url, '/home/stud125/project/Data_Literacy/src/example.json')

if __name__ == "__main__":
    main()