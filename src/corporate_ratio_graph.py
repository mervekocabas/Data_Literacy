import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr
import matplotlib.font_manager as fm
import matplotlib.gridspec as gridspec

prop = fm.FontProperties(fname='C:/Windows/Fonts/times.ttf')  # Adjust path if necessary
plt.rcParams['font.family'] = prop.get_name()

# Load the dataset
file_path = "../data/merged_dataset_v0.csv"
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
# plt.figure(figsize=(8, 6))  # Adjust width and height as needed
custom_colors= {
    "CVPR": "#922B21",  # Dark Brown
    "ICCV": "#1B4F72",  # Dark Blue
    "WACV":  "#5B3A29", # Dark Red
    "Total": "#008B8B"  # Dark Turquoise
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
    linewidth=2,  # Adjust line width
    palette=custom_colors
)

# Customize the plot
# plt.title("Corporate Affiliated Paper Ratio Over the Years by Conference", fontsize=16)
plt.ylabel("Corporate Affiliated Paper Ratio", fontsize=20, fontweight='medium')
plt.xlabel("Year", fontsize=20, fontweight='medium')
plt.legend(title="Conference Name",title_fontsize='15',loc="upper left", bbox_to_anchor=(0.65, 0.71), fontsize=14, frameon=False) 
plt.tight_layout(pad=2)

plt.xticks(fontsize=18)  # Resize x-axis labels
plt.yticks(fontsize=18)  # Resize y-axis labels
sns.despine() 

# Save the plot

output_file_path = "../graphs/corporate_ratio_graph_final.png"
plt.savefig(output_file_path, dpi=300)

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

# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# import numpy as np
# from scipy.stats import spearmanr
# import matplotlib.font_manager as fm
# import matplotlib.gridspec as gridspec

# # Set font properties (Adjust path if necessary)
# prop = fm.FontProperties(fname="C:/Windows/Fonts/times.ttf")
# plt.rcParams["font.family"] = prop.get_name()

# # Load the dataset
# file_path = "../data/merged_dataset_v0.csv"
# data = pd.read_csv(file_path)

# # Ensure conferences have data for correct years
# valid_years = {
#     "cvpr": [2019, 2020, 2021, 2022, 2023, 2024],
#     "iccv": [2019, 2021, 2023],
#     "wacv": [2020, 2021, 2022, 2023, 2024],
# }

# # Filter data to keep only valid years for each conference
# data_filtered = data[data.apply(lambda x: x["Conference"].lower() in valid_years and x["Year"] in valid_years[x["Conference"].lower()], axis=1)]

# # Group by Year, Conference, and PaperType to count papers
# grouped_counts = data_filtered.groupby(["Year", "Conference", "PaperType"]).size().reset_index(name="Count")

# # Pivot the data for company/academia counts
# pivot_table = grouped_counts.pivot(index=["Year", "Conference"], columns="PaperType", values="Count").fillna(0)

# # Compute company/academia ratio
# pivot_table["Company_Academia_Ratio"] = pivot_table["Company"] / (pivot_table["Academia"] + pivot_table["Company"])

# # Reset index for plotting
# pivot_table = pivot_table.reset_index()

# # Convert conference names to uppercase for plotting
# pivot_table["Conference"] = pivot_table["Conference"].str.upper()

# # Initialize dictionary to store Spearman correlation results
# spearman_results = {}

# # Compute yearly aggregated data for all conferences
# yearly_aggregated = pivot_table.groupby("Year").agg({"Company": "sum", "Academia": "sum"}).reset_index()

# # Compute total company/academia ratio
# yearly_aggregated["Company_Academia_Ratio"] = yearly_aggregated["Company"] / (yearly_aggregated["Academia"] + yearly_aggregated["Company"])

# # Add total data to the pivot table
# pivot_table = pd.concat([pivot_table, yearly_aggregated.assign(Conference="Total")])

# # Compute Spearman's Rank Correlation for each conference
# for conference in pivot_table["Conference"].unique():
#     conf_data = pivot_table[pivot_table["Conference"] == conference]
#     spearman_corr, p_value = spearmanr(conf_data["Year"], conf_data["Company_Academia_Ratio"])
#     spearman_results[conference] = {
#         "Spearman Rank Correlation": spearman_corr,
#         "P-value": p_value,
#     }

# # --- Create the Figure ---
# fig = plt.figure(figsize=(12, 6))
# gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])  # 2:1 layout

# # --- Graph on the Left ---
# ax1 = fig.add_subplot(gs[0])

# # Define custom line styles
# line_styles = {"WACV": (2, 2), "ICCV": (5, 5), "CVPR": (3, 1), "Total": (1, 1)}

# custom_colors = {
#     "WACV": "#1f77b4",  # Blue
#     "ICCV": "#ff7f0e",  # Orange
#     "CVPR": "#2ca02c",  # Green
#     "Total": "#d62728"  # Red
# }

# sns.lineplot(
#     data=pivot_table,
#     x="Year",
#     y="Company_Academia_Ratio",
#     hue="Conference",
#     style="Conference",
#     markers=True,
#     dashes=[line_styles[c] for c in pivot_table["Conference"].unique()],
#     markersize=8,
#     linewidth=2,
#     ax=ax1,
#     palette=custom_colors
# )

# # Formatting
# ax1.set_ylabel("Corporate Affiliated Paper Ratio", fontsize=16)
# ax1.set_xlabel("Year", fontsize=16)
# ax1.legend(title="Conference", fontsize=12, loc="upper left", bbox_to_anchor=(0.65, 0.8), frameon=False)
# ax1.grid(True, linestyle="--", alpha=0.5)
# ax1.set_xticks(sorted(pivot_table["Year"].unique()))  # Ensure correct x-ticks
# sns.despine()

# # --- Table on the Right ---
# ax2 = fig.add_subplot(gs[1])
# ax2.axis("tight")
# ax2.axis("off")

# # Prepare table data
# table_data = [
#     [conf, f"{res['Spearman Rank Correlation']:.3f}", f"{res['P-value']:.3f}*"]
#     for conf, res in spearman_results.items()
# ]

# # Define column labels with a **double-line header**
# col_labels = ["Conference", "Spearman’s Rank\nCorrelation Coefficient", "P-value"]

# # Create the table
# table = ax2.table(
#     cellText=table_data,
#     colLabels=col_labels,
#     loc="center",
#     cellLoc="center",
#     colColours=["#f2f2f2"] * 3,  # Light gray header
# )

# table.auto_set_font_size(False)
# table.set_fontsize(14)
# table.auto_set_column_width([0, 1, 2])  # Adjust column width
# # Increase height for the header row
# for col in range(3):  # Loop through each column
#     table._cells[(0, col)].set_height(0.07)  # Increase height for header row
#     table._cells[(0, col)].set_fontsize(14)  # Slightly larger font for header
# # Save the combined figure
# output_file_path = "../graphs/corporate_ratio_with_table.png"
# plt.tight_layout()
# plt.savefig(output_file_path, dpi=300, bbox_inches="tight", transparent=False)

# # Show the figure
# # plt.show()

# # Print Spearman results
# for conference, results in spearman_results.items():
#     print(f"Spearman Results for {conference}:")
#     print(f"  Spearman Rank Correlation: {results['Spearman Rank Correlation']:.4f}")
#     print(f"  P-value: {results['P-value']:.4f}")
#     if results["P-value"] < 0.05:
#         print(f"  There is a significant monotonic relationship between year and corporate paper ratio for {conference}.")
#     else:
#         print(f"  There is no significant monotonic relationship between year and corporate paper ratio for {conference}.")
#     print()