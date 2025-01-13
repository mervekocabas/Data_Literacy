import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

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
pivot_table["Company_Academia_Ratio"] = pivot_table["Company"] / (pivot_table["Academia"] + pivot_table["Company"])

# Reset the index for plotting
pivot_table = pivot_table.reset_index()

# Convert conference names to uppercase for plotting
pivot_table["Conference"] = pivot_table["Conference"].str.upper()

# Prepare the data for regression
regression_results = {}
for conference in pivot_table["Conference"].unique():
    conf_data = pivot_table[pivot_table["Conference"] == conference]
    X = conf_data["Year"].values.reshape(-1, 1)  # Reshape to 2D for sklearn
    y = conf_data["Company_Academia_Ratio"].values

    # Fit a linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Store regression results
    regression_results[conference] = {
        "slope": model.coef_[0],
        "intercept": model.intercept_,
        "r_squared": model.score(X, y)
    }

    # Add the regression line predictions
    pivot_table.loc[pivot_table["Conference"] == conference, "Trend"] = model.predict(X)

# Plot the trends of company/academia ratio over the years
plt.figure(figsize=(12, 6))

# Plot the original data with gapped lines
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
    },
    markersize=10,  # Adjust marker size
    linewidth=2  # Adjust line width
)

# Add regression trendlines as solid lines
for conference in pivot_table["Conference"].unique():
    conf_data = pivot_table[pivot_table["Conference"] == conference]
    plt.plot(
        conf_data["Year"],
        conf_data["Trend"],
        label=f"{conference} Trend",
        linestyle="-",  # Solid line for trend
        linewidth=2,  # Make regression line slightly thicker
        alpha=0.8  # Add transparency to keep the plot clean
    )

# Customize the plot
plt.title("Corporate Affiliated Paper Ratio Over the Years by Conference", fontsize=18, weight='bold')
plt.ylabel("Corporate Affiliated Paper Ratio", fontsize=14)
plt.xlabel("Year", fontsize=14)
plt.legend(title="Conference Name", title_fontsize=14, fontsize=12, loc="upper left", bbox_to_anchor=(1, 1))  # Move legend outside
plt.xticks(fontsize=12)  # Resize x-axis labels
plt.yticks(fontsize=12)  # Resize y-axis labels
plt.tight_layout()

# Save the plot
output_file_path = "../graphs/corporate_ratio_graph_with_regression.png"
plt.savefig(output_file_path)

# Print regression results
print("Regression Results:")
for conference, results in regression_results.items():
    print(f"{conference}: Slope = {results['slope']:.4f}, Intercept = {results['intercept']:.4f}, R^2 = {results['r_squared']:.4f}")
