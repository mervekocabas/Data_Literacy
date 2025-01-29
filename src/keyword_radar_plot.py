import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from textwrap import wrap


def plot_radarline_chart(keyword_counts):
    total_university_papers = sum(counts['university'] for counts in keyword_counts.values())
    total_company_papers = sum(counts['company'] for counts in keyword_counts.values())

    # Normalize university and company counts within each group
    normalized_counts = {
        group: {
            "university": counts["university"] / total_university_papers,
            "company": counts["company"] / total_company_papers
        }
        for group, counts in keyword_counts.items()
    }

    # Sort groups alphabetically for consistency
    groups = sorted(normalized_counts.keys())
    university_values = [normalized_counts[group]["university"] for group in groups]
    company_values = [normalized_counts[group]["company"] for group in groups]

    # Ensure the plot is circular by closing the loop
    university_values.append(university_values[0])
    company_values.append(company_values[0])
    angles = np.linspace(0, 2 * np.pi, len(groups), endpoint=False).tolist()
    angles += angles[:1]

    GREY12 = "#1f1f1f"
    company_color = "#4c78a8"
    university_color = "#e57f4e"

    # Initialize layout in polar coordinates
    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw={"projection": "polar"})

    # Set background color to white, both axis and figure.
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.set_theta_offset(1.2 * np.pi / 2)

    # Plot line for company papers
    ax.plot(angles, company_values, color=company_color, linewidth=2, linestyle='solid', label='Corporate Papers')

    # Plot line for university papers
    ax.plot(angles, university_values, color=university_color, linewidth=1, linestyle='solid', label='Academia Papers')

    # Wrap categories for better visualization
    wrapped_categories = ["\n".join(wrap(r, 7, break_long_words=False)) for r in groups]

    # Add a label for the first category to close the loop
    wrapped_categories += [wrapped_categories[0]]

    # Set the labels with reduced size
    ax.set_xticks(angles)
    ax.set_xticklabels(wrapped_categories, size=8)  # Reduce size of labels to 8

    # Add a legend with reduced font size
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1), fontsize=8)  # Reduce font size of the legend

    # Set the title of the chart
    ax.set_title('Comparison of Corporate and Academia Papers in Keyword Categories', fontsize=12)

    # Show the plot
    plt.tight_layout()
    # plt.show()
    
def plot_radar_chart(keyword_counts):
    total_university_papers = sum(counts['university'] for counts in keyword_counts.values())
    total_company_papers = sum(counts['company'] for counts in keyword_counts.values())

    # Normalize university and company counts within each group
    normalized_counts = {
        group: {
            "university": counts["university"] / total_university_papers,
            "company": counts["company"] / total_company_papers
        }
        for group, counts in keyword_counts.items()
    }

    # Sort groups alphabetically for consistency
    groups = sorted(normalized_counts.keys())
    university_values = [normalized_counts[group]["university"] for group in groups]
    company_values = [normalized_counts[group]["company"] for group in groups]

    # Ensure the plot is circular by closing the loop
    angles = np.linspace(0, 2 * np.pi, len(groups), endpoint=False).tolist()

    company_color = "#4c78a8"
    university_color = "#e57f4e"

    # Initialize layout in polar coordinates
    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw={"projection": "polar"})

    # Set background color
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.set_theta_offset(1.2 * np.pi / 2)

    # Plot dynamically so the smaller bar is on top
    for i in range(len(groups)):
        if university_values[i] < company_values[i]:
            ax.bar(angles[i], company_values[i], color=company_color, alpha=1, width=0.2, zorder=9, label='Corporate Papers' if i == 0 else "")
            ax.bar(angles[i], university_values[i], color=university_color, alpha=1, width=0.2, zorder=9, label="Academia Papers" if i == 0 else "")
        else:
            ax.bar(angles[i], university_values[i], color=university_color, alpha=1, width=0.2, zorder=9, label="Academia Papers" if i == 0 else "")
            ax.bar(angles[i], company_values[i], color=company_color, alpha=1, width=0.2, zorder=9, label="Corporate Papers" if i == 0 else "")

    # Wrap categories for better visualization
    wrapped_categories = ["\n".join(wrap(r, 8, break_long_words=False)) for r in groups]

    # Set the labels with reduced size
    ax.set_xticks(angles)
    ax.set_xticklabels(wrapped_categories, size=8)

    # Add a legend with reduced font size
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1), fontsize=8)

    # Set the title of the chart
    ax.set_title('Comparison of Corporate and Academia Papers in Keyword Categories', fontsize=12)

    # Show the plot
    plt.tight_layout()
    # plt.show()
    plt.savefig("C:\\Users\\JAI GURU JI\\Desktop\\Data Lit\\Project\\Data_Literacy\\graphs\\radar_bar_plot_final.png")

# Read CSV file and process data
csv_file = "C:\\Users\\JAI GURU JI\\Desktop\\Data Lit\\Project\\Data_Literacy\\data\\combined_results.csv"  # Change this to the actual filename
df = pd.read_csv(csv_file)
df = df.drop([5, 19, 15, 13, 10, 11])
# Convert the data into a dictionary format for the function
keyword_counts = {
    row["Keyword"]: {"university": row["University Papers"], "company": row["Company Papers"]}
    for _, row in df.iterrows()
}

# Call the function with the processed data
plot_radar_chart(keyword_counts)
# plot_radarline_chart(keyword_counts)