import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from textwrap import wrap

# Load the data
df = pd.read_csv('C:\\Users\\JAI GURU JI\\Desktop\\Data Lit\\Project\\Data_Literacy\\data\\combined_results.csv')

# Data from the CSV
categories = df['Keyword'].tolist()
company_papers = df['Company Papers'].tolist()
university_papers = df['University Papers'].tolist()

# Normalize the data (scale between 0 and 1)
max_value = max(max(company_papers), max(university_papers))
company_papers_normalized = [x / max_value for x in company_papers]
university_papers_normalized = [x / max_value for x in university_papers]

# Number of categories
N = len(categories)

# Angles for radar chart
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()

# Ensure the plot is circular by closing the loop
company_papers_normalized += company_papers_normalized[:1]
university_papers_normalized += university_papers_normalized[:1]
angles += angles[:1]

GREY12 = "#1f1f1f"

# Set default font to Bell MT
# plt.rcParams.update({"font.family": "Bell MT"})

# Set default font color to GREY12
plt.rcParams["text.color"] = GREY12

# The minus glyph is not available in Bell MT
# This disables it, and uses a hyphen
plt.rc("axes", unicode_minus=False)

# Colors
company_color = "#6C5B7B"
university_color = "#F67280"

# Some layout stuff ----------------------------------------------
# Initialize layout in polar coordinates
fig, ax = plt.subplots(figsize=(9, 9), subplot_kw={"projection": "polar"})

# Set background color to white, both axis and figure.
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

ax.set_theta_offset(1.2 * np.pi / 2)
ax.set_ylim(-0.2, 1)  # Keep the y-axis between 0 and 1 for normalized data

# Add bars for company papers
ax.bar(angles, company_papers_normalized, color=company_color, alpha=0.7, width=0.4, zorder=10, label='Company Papers')

# Add bars for university papers
ax.bar(angles, university_papers_normalized, color=university_color, alpha=0.7, width=0.4, zorder=9, label='University Papers')

# Wrap categories for better visualization
wrapped_categories = ["\n".join(wrap(r, 5, break_long_words=False)) for r in categories]

# Add a label for the first category to close the loop
wrapped_categories += [wrapped_categories[0]]

# Set the labels with reduced size
ax.set_xticks(angles)
ax.set_xticklabels(wrapped_categories, size=8)  # Reduce size of labels to 8

# Add a legend with reduced font size
ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1), fontsize=10)  # Reduce font size of the legend

ax.set_title('Comparison of Company and University Papers in Various Categories (CVPR, ICCV, WACV)', fontsize=12)

# Show the plot
plt.tight_layout()
# plt.show()
plt.savefig('C:\\Users\\JAI GURU JI\\Desktop\\Data Lit\\Project\\Data_Literacy\\graphs\\keywords_radar_plot.png', dpi=300)


# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# from textwrap import wrap

# # Load the data
# df = pd.read_csv('C:\\Users\\JAI GURU JI\\Desktop\\Data Lit\\Project\\Data_Literacy\\data\\combined_results.csv')

# # Data from the CSV
# categories = df['Keyword'].tolist()
# company_papers = df['Company Papers'].tolist()
# university_papers = df['University Papers'].tolist()

# # Normalize the data so that each category's "Company Papers" and "University Papers" sum to 1
# total_papers = np.array(company_papers) + np.array(university_papers)

# # Avoid division by zero in case any total_papers value is 0
# company_papers_normalized = np.array(company_papers) / total_papers
# university_papers_normalized = np.array(university_papers) / total_papers

# # Number of categories
# N = len(categories)

# # Angles for radar chart
# angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()

# # Ensure the plot is circular by closing the loop
# company_papers_normalized = np.concatenate([company_papers_normalized, [company_papers_normalized[0]]])
# university_papers_normalized = np.concatenate([university_papers_normalized, [university_papers_normalized[0]]])
# angles += angles[:1]

# GREY12 = "#1f1f1f"

# # Set default font color to GREY12
# plt.rcParams["text.color"] = GREY12

# # The minus glyph is not available in Bell MT
# # This disables it, and uses a hyphen
# plt.rc("axes", unicode_minus=False)

# # Colors
# company_color = "#6C5B7B"
# university_color = "#F67280"

# # Some layout stuff ----------------------------------------------
# # Initialize layout in polar coordinates
# fig, ax = plt.subplots(figsize=(9, 9), subplot_kw={"projection": "polar"})

# # Set background color to white, both axis and figure.
# fig.patch.set_facecolor("white")
# ax.set_facecolor("white")

# ax.set_theta_offset(1.2 * np.pi / 2)
# ax.set_ylim(-0.2, 1)  # Keep the y-axis between 0 and 1 for normalized data

# # Add bars for company papers
# ax.bar(angles, company_papers_normalized, color=company_color, alpha=0.7, width=0.4, zorder=10, label='Company Papers')

# # Add bars for university papers
# ax.bar(angles, university_papers_normalized, color=university_color, alpha=0.7, width=0.4, zorder=9, label='University Papers')

# # Wrap categories for better visualization
# wrapped_categories = ["\n".join(wrap(r, 5, break_long_words=False)) for r in categories]

# # Add a label for the first category to close the loop
# wrapped_categories += [wrapped_categories[0]]

# # Set the labels with reduced size
# ax.set_xticks(angles)
# ax.set_xticklabels(wrapped_categories, size=8)  # Reduce size of labels to 8

# # Add a legend with reduced font size
# ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1), fontsize=10)  # Reduce font size of the legend

# # Add a title to the plot
# ax.set_title('Comparison of Company and University Papers in Various Categories (CVPR, ICCV, WACV)', fontsize=12)

# # Show the plot
# plt.tight_layout()
# # plt.show()  # Uncomment to display the plot

# # Save the plot as an image file
# plt.savefig('C:\\Users\\JAI GURU JI\\Desktop\\Data Lit\\Project\\Data_Literacy\\graphs\\keywords_radar_plot_2.png', dpi=300)
