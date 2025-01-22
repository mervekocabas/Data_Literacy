import pandas as pd

# List of CSV files
csv_files = [
    'C:\\Users\\JAI GURU JI\\Desktop\\Data Lit\\Project\\Data_Literacy\\data\\cvpr_preprocessed\\final_cvpr_results.csv',
    'C:\\Users\\JAI GURU JI\\Desktop\\Data Lit\\Project\\Data_Literacy\\data\\iccv_preprocessed\\final_iccv_results.csv',
    'C:\\Users\\JAI GURU JI\\Desktop\\Data Lit\\Project\\Data_Literacy\\data\\wacv_preprocessed\\final_wacv_results.csv',
]

dataframes = [pd.read_csv(file) for file in csv_files]

# Concatenate all DataFrames
all_data = pd.concat(dataframes)

# Assuming the first column is 'Keyword' and the rest are numeric values to sum
# Group by 'Keyword' and sum the numeric columns
summed_data = all_data.groupby('Keyword').sum().reset_index()

# Check the final dataframe after summing
summed_data.to_csv('C:\\Users\\JAI GURU JI\\Desktop\\Data Lit\\Project\\Data_Literacy\\data\\combined_results.csv', index=False)
