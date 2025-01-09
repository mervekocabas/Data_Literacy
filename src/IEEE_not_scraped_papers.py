import csv

def extract_empty_index_terms(input_csv, output_txt):
    """
    Extract the names of papers with empty 'ieee_index_terms' and write them to a text file.

    Args:
        input_csv (str): Path to the input CSV file.
        output_txt (str): Path to the output text file.
    """
    try:
        papers_with_empty_terms = []
        
        # Read the CSV file
        with open(input_csv, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                # Check if 'ieee_index_terms' is empty
                if not row.get('ieee_index_terms') or row['ieee_index_terms'].strip() == '':
                    papers_with_empty_terms.append(row['title'])
        
        # Write the paper names to the text file
        with open(output_txt, 'w', encoding='utf-8') as outfile:
            outfile.write("\n".join(papers_with_empty_terms))
        
        print(f"Extracted {len(papers_with_empty_terms)} papers with empty 'ieee_index_terms' into {output_txt}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_csv = '/Users/merve/Data_Literacy/data/iccv_preprocessed/iccv2019.csv'  # Input CSV file path
    output_txt = '/Users/merve/Data_Literacy/data/iccv_preprocessed/papers_with_empty_index_terms_2019.txt'  # Output TXT file path
    extract_empty_index_terms(input_csv, output_txt)
