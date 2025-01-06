import os
import re
import pandas as pd

def create_dataset(data_folder = "data", output_file='merged_dataset.csv'):
    """
    Merges all CSV files from subfolders containing 'preprocessed' in their names
    into a single pandas DataFrame. Adds a column for the year extracted from filenames.
    
    Parameters:
    - data_folder (str): Path to the main data folder.
    - output_file (str): Name of the output CSV file. Defaults to 'merged_dataset.csv'.
    
    Returns:
    - pd.DataFrame: The merged pandas DataFrame.
    """
    # Initialize an empty list to store dataframes
    dataframes = []

    # Walk through the directory
    for root, dirs, files in os.walk(data_folder):
        # Check if the current folder contains 'preprocessed'
        if 'preprocessed' in root.lower():
            # Iterate over files in this folder
            for file in files:
                if file.endswith('.csv'):  # Check if the file is a CSV
                    file_path = os.path.join(root, file)
                    print(f"Reading file: {file_path}")
                    # Read the CSV file
                    df = pd.read_csv(file_path)
                    # Extract year from the filename (e.g., 'cvpr2019.csv' -> '2019')
                    year = ''.join(filter(str.isdigit, os.path.splitext(file)[0]))
                    match = re.match(r"([a-zA-Z]+)(\d+)", os.path.splitext(file)[0])
                    if match:
                        conference = match.group(1) 
                        df["Conference"] = conference
                    year = ''.join(filter(str.isdigit, os.path.splitext(file)[0]))
                    # Add the year column to the DataFrame
                    df['Year'] = year
                    # Append the DataFrame to the list
                    dataframes.append(df)

    # Merge all dataframes into one
    if dataframes:
        merged_df = pd.concat(dataframes, ignore_index=True)
        print(f"Merged dataframe created with {len(merged_df)} rows.")
    else:
        print("No CSV files found in preprocessed folders.")
        return pd.DataFrame()  # Return an empty DataFrame if no files found

    # Save the merged dataframe to a CSV file
    output_path = os.path.join(data_folder, output_file)
    merged_df.to_csv(output_path, index=False)
    print(f"Merged dataset saved to: {output_path}")
    
    return merged_df

# df = create_dataset()