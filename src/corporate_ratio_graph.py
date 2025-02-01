import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr


# Load the dataset
file_path = "../data/merged_v1.csv"
data = pd.read_csv(file_path)

# Ensure conferences have data for correct years
valid_years = {
    "cvpr": [2019, 2020, 2021, 2022, 2023, 2024],
    "iccv": [2019, 2021, 2023],
    "wacv": [2020, 2021, 2022, 2023, 2024]
}

# Filter the data to keep only valid years for each conference
data_filtered = data[data.apply(lambda x: x["Conference"].lower() in valid_years and x["Year"] in valid_years[x["Conference"].lower()], axis=1)]

# Group by Year, Conference, and PaperType to count the number of papers
grouped_counts = data_filtered.groupby(["Year", "Conference", "PaperType"]).size().reset_index(name="Count")

# Pivot the data to get counts for "Company" and "Academia" side-by-side
pivot_table = grouped_counts.pivot(index=["Year", "Conference"], columns="PaperType", values="Count").fillna(0)

# Calculate the company/academia ratio
pivot_table["Company_Academia_Ratio"] = pivot_table["Company"] / (pivot_table["Academia"] + pivot_table["Company"])

# Reset the index for plotting
pivot_table = pivot_table.reset_index()

# Convert conference names to uppercase for plotting
pivot_table["Conference"] = pivot_table["Conference"].str.upper()

# Initialize an empty dictionary to store results
spearman_results = {}

# Now, compute the yearly aggregated data for all conferences
yearly_aggregated = pivot_table.groupby("Year").agg({
    'Company': 'sum',
    'Academia': 'sum'
}).reset_index()

# Calculate the total company/academia ratio across all conferences
yearly_aggregated["Company_Academia_Ratio"] = yearly_aggregated["Company"] / (yearly_aggregated["Academia"] + yearly_aggregated["Company"])

# Add the aggregated data to the pivot table for plotting
pivot_table = pd.concat([pivot_table, yearly_aggregated.assign(Conference='Total')])

# Calculate Spearman's Rank Correlation and Mann-Kendall for each conference and the total
for conference in pivot_table["Conference"].unique():
    # Filter the data for the current conference (or Total for overall data)
    conf_data = pivot_table[pivot_table["Conference"] == conference]
    
    # Calculate Spearman Rank Correlation for the current conference
    spearman_corr, p_value = spearmanr(conf_data['Year'], conf_data['Company_Academia_Ratio'])
    
    # Store the results in the dictionary
    spearman_results[conference] = {
        'Spearman Rank Correlation': spearman_corr,
        'P-value': p_value
    }


# Assuming you have a DataFrame `pivot_table` ready for plotting
sns.lineplot(
    data=pivot_table,
    x="Year",
    y="Company_Academia_Ratio",
    hue="Conference",
    style="Conference",  # Different markers for each conference
    markers=True,  # Enable markers
    dashes={
        'WACV': (2, 2),  # Dash pattern for WACV
        'ICCV': (5, 5),  # Dash pattern for ICCV
        'CVPR': (3, 1),  # Dash pattern for CVPR
        'Total': (1, 1)   # Solid line for Total
    },
    markersize=10,  # Adjust marker size
    linewidth=2  # Adjust line width
)

# Customize the plot
plt.title("Corporate Affiliated Paper Ratio Over the Years by Conference")
plt.ylabel("Corporate Affiliated Paper Ratio")
plt.xlabel("Year")
plt.legend(title="Conference Name",loc="upper left", bbox_to_anchor=(1, 1))  # Move legend outside
plt.tight_layout()

# Save the plot
output_file_path = "../graphs/corporate_ratio_graph_final.png"
plt.savefig(output_file_path)

# Print the Spearman results
for conference, results in spearman_results.items():
    print(f"Spearman Results for {conference}:")
    print(f"  Spearman Rank Correlation: {results['Spearman Rank Correlation']:.4f}")
    print(f"  P-value: {results['P-value']:.4f}")
    if results['P-value'] < 0.05:
        print(f"  There is a significant monotonic relationship between year and corporate paper ratio for {conference}.")
    else:
        print(f"  There is no significant monotonic relationship between year and corporate paper ratio for {conference}.")
    print()