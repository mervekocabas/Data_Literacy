import numpy as np
import matplotlib.pyplot as plt
from math import pi
import pandas as pd

# Load the data from CSV
df = pd.read_csv('C:\\Users\\JAI GURU JI\\Desktop\\Data Lit\\Project\\Data_Literacy\\data\\wacv_preprocessed\\results_20.csv')

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

# Plotting
fig, ax = plt.subplots(figsize=(10, 10), dpi=80, subplot_kw=dict(polar=True))

# Plot company papers (normalized)
ax.plot(angles, company_papers_normalized, linewidth=2, linestyle='solid', label='Company Papers', color='blue')

# Plot university papers (normalized)
ax.plot(angles, university_papers_normalized, linewidth=2, linestyle='solid', label='University Papers', color='red')

# Fill the areas
ax.fill(angles, company_papers_normalized, color='blue', alpha=0.25)
ax.fill(angles, university_papers_normalized, color='red', alpha=0.25)

# Add labels
ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=10, rotation=45, ha="left")

# Add radial ticks (with normalized values)
num_ticks = 5  # Number of ticks you want on the radial axis
radial_ticks = np.linspace(0, 1, num_ticks + 1)  # Generate ticks from 0 to 1
ax.set_yticks(radial_ticks)  # Set the ticks along the radial axis

# Optionally, add radial tick labels (from 0 to 1)
ax.set_yticklabels([str(round(x, 2)) for x in radial_ticks])  # Labels each tick with the corresponding value

# Title and legend
plt.title('Comparison of Company and University Papers in Various Categories WAVCV 2020', size=16)
plt.legend(loc='lower right', bbox_to_anchor=(1.1, 0.1))

# Show plot
plt.tight_layout()
# plt.show()
plt.savefig('C:\\Users\\JAI GURU JI\\Desktop\\Data Lit\\Project\\Data_Literacy\\graphs\\keywords_radar_plot.png')
