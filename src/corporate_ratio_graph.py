import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = "../data/merged_dataset.csv"
data = pd.read_csv(file_path)

# Classify papers as "Company" or "Academia"
data["PaperType"] = data["company_affiliation"].apply(lambda x: "Company" if x > 0 else "Academia")

# Group by Year, Conference, and PaperType to count the number of papers
grouped_counts = data.groupby(["Year", "Conference", "PaperType"]).size().reset_index(name="Count")

# Pivot the data to get counts for "Company" and "Academia" side-by-side
pivot_table = grouped_counts.pivot(index=["Year", "Conference"], columns="PaperType", values="Count").fillna(0)

# Calculate the company/academia ratio
pivot_table["Company_Academia_Ratio"] = pivot_table["Company"] / (pivot_table["Academia"]+pivot_table["Company"])

# Reset the index for plotting
pivot_table = pivot_table.reset_index()

# Convert conference names to uppercase for plotting
pivot_table["Conference"] = pivot_table["Conference"].str.upper()

# Plot the trends of company/academia ratio over the years
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=pivot_table,
    x="Year",
    y="Company_Academia_Ratio",
    hue="Conference",
    style="Conference",  # Different markers for each conference
    markers=True,  # Enable markers
    markersize=10  # Adjust marker size
)

# Customize the plot
plt.title("Corporate Affiliated Paper Ratio Over the Years by Conference", fontsize=18, weight='bold')
plt.ylabel("Corporate Affiliated Paper Ratio", fontsize=14)
plt.xlabel("Year", fontsize=14)
plt.legend(title="Conference Name", title_fontsize=14, fontsize=12)  # Adjust legend font sizes
plt.xticks(fontsize=12) # rotation=45  # Rotate and resize x-axis labels
plt.yticks(fontsize=12)  # Resize y-axis labels
plt.tight_layout()
plt.show()
