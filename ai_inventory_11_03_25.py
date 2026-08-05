# -*- coding: utf-8 -*-
"""ai-inventory-11-03-25.ipynb

This script analyzes Federal AI Use Case Inventories from 2023, 2024, and 2025.
It performs data loading, cleaning, identification of common and duplicate use cases,
and generates visualizations and Excel reports summarizing the findings.

Original file is located at
    https://colab.research.google.com/drive/1CBjBEic1TOWQd2qc-nNvOZAdLIKxslAC

Read in 2023, 2024, and 2025 AI use case inventories.
"""

from datetime import datetime
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import string
import seaborn as sns

# Read in 2023 AI use case inventory converted into excel file from https://github.com/ombegov/2024-Federal-AI-Use-Case-Inventory/blob/main/data/2023_consolidated_ai_inventory_raw.csv
file_name = "./inventories/2023_consolidated_ai_inventory_raw.xlsx"
inventory_2023 = pd.read_excel(file_name, header=1, keep_default_na=False)


# Read in 2024 AI use case inventory from https://github.com/ombegov/2024-Federal-AI-Use-Case-Inventory/blob/main/data/2024_consolidated_ai_inventory_raw_v2.xls
file_name = "./inventories/2024_consolidated_ai_inventory_raw_v2.xls"
inventory_2024 = pd.read_excel(file_name, header=0, keep_default_na=False)
# inventory_2024["Use Case Topic Area"] = inventory_2024["Use Case Topic Area"].fillna("None")
# inventory_2024["Is the AI use case rights-impacting, safety-impacting, both, or neither?"] = inventory_2024["Is the AI use case rights-impacting, safety-impacting, both, or neither?"].fillna("None")

# Read in 2025 AI use case inventory from https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory/blob/main/Data/2025_individually_reported_AI_use_cases.xlsx
file_name = "./inventories/2025_individually_reported_AI_use_cases.xlsx"
inventory_2025 = pd.read_excel(file_name, header=1, keep_default_na=False)
# inventory_2025["Use Case Topic Area"] = inventory_2025["Use Case Topic Area"].fillna("None")
# inventory_2025["Is the AI use case high-impact?"] = inventory_2025["Is the AI use case high-impact?"].fillna("None")

# Clean up dataframes: remove nan values, strip leading/trailing whitespace from all string values and column names
inventory_2023 = inventory_2023.replace(r'^\s*$', np.nan, regex=True)
inventory_2024 = inventory_2024.replace(r'^\s*$', np.nan, regex=True)
inventory_2025 = inventory_2025.replace(r'^\s*$', np.nan, regex=True)
inventory_2023 = inventory_2023.map(lambda x: x.strip() if isinstance(x, str) else x)
inventory_2024 = inventory_2024.map(lambda x: x.strip() if isinstance(x, str) else x)
inventory_2025 = inventory_2025.map(lambda x: x.strip() if isinstance(x, str) else x)
inventory_2023 = inventory_2023.replace(["N/A", "NA"], "Not Applicable")
inventory_2024 = inventory_2024.replace(["N/A", "NA"], "Not Applicable")
inventory_2025 = inventory_2025.replace(["N/A", "NA"], "Not Applicable")
inventory_2023.fillna("None", inplace=True)
inventory_2024.fillna("None", inplace=True)
inventory_2025.fillna("None", inplace=True)
inventory_2023.columns = inventory_2023.columns.str.strip()
inventory_2024.columns = inventory_2024.columns.str.strip()
inventory_2025.columns = inventory_2025.columns.str.strip()

"""Count the number of use cases in 2023, 2024, and 2025."""
print(len(inventory_2023))
print(len(inventory_2024))
print(len(inventory_2025))

"""Temporary code to determine whether certain fields correspond to data subsets."""
# inventory_2025_not_fd_hi = inventory_2025[~((inventory_2025["Stage of Development"].str.startswith(("d) Retired", "c) Deployed"))) &
# (inventory_2025["Is the AI use case high-impact?"].isin(["a) High-impact", "b) Presumed high-impact, but determined not high impact"])))]
# inventory_2025_final = inventory_2025_not_fd_hi.loc[:, inventory_2025_not_fd_hi.notna().any()]
# print(inventory_2025_final.columns)
# print(inventory_2025_final.shape)

"""Definitions"""

# Returns a plot
def create_plot(topic_indices, topic_values, topic_name, data_subset, inventory_year, sub_topic_counts=None):
  """
  Generates and saves a horizontal bar plot comparing AI use case topic areas.

  Args:
    topic_indices (list): List of topic labels for the y-axis.
    topic_values (list): List of total use case counts for each topic.
    topic_name (str): The name of the topic being plotted (e.g., "Use Case Topic Area").
    data_subset (str): Description of the data subset (e.g., "Full Inventory", "Department of Energy").
    inventory_year (str): The year of the inventory (e.g., "2024").
    sub_topic_counts (list, optional): List of counts for a sub-category (e.g., rights/safety-impacting). Defaults to None.
  """

  fig, ax = plt.subplots(figsize=(10, 7))
  
  y = np.arange(len(topic_indices))
  bar_height = 0.35
  
  bars_total = ax.barh(y + bar_height / 2, topic_values, bar_height,
                      label='All use cases',
                      color='#378ADD', zorder=3)
  
  if (sub_topic_counts):
    bars_sub = ax.barh(y - bar_height / 2, sub_topic_counts, bar_height,
                      label='Rights/safety-impacting',
                      color='#D85A30', zorder=3)

  # Compute a dynamic x-limit that gives room for value labels
  all_values = list(topic_values)
  if sub_topic_counts:
      all_values += list(sub_topic_counts)
  max_val = max(all_values) if all_values else 0
  x_max = max_val * 1.15   # 15% right-side padding for the text labels
  
  # Value labels
  for bar in bars_total:
      w = bar.get_width()
      if w > 0:
          ax.text(w + 1.2, bar.get_y() + bar.get_height() / 2,
                  str(int(w)), va='center', ha='left', fontsize=10, color='#333')
  
  if (sub_topic_counts):
    for bar in bars_sub:
        w = bar.get_width()
        if w > 0:
            ax.text(w + 1.2, bar.get_y() + bar.get_height() / 2,
                    str(int(w)), va='center', ha='left', fontsize=10, color='#333')
  
  ax.set_yticks(y)
  ax.set_yticklabels(topic_indices, fontsize=11)
  ax.invert_yaxis()
  ax.set_xlabel("Number of use cases", fontsize=11)
  ax.set_title(topic_name + '\n' + data_subset + '\n(' + inventory_year + ' Federal AI Use Case Inventory)',
              fontsize=13, fontweight='bold', pad=14)
  ax.set_xlim(0, x_max)
  ax.xaxis.grid(True, color='#e0e0e0', zorder=0)
  ax.set_axisbelow(True)
  ax.spines[['top', 'right', 'left']].set_visible(False)
  
  if (sub_topic_counts):
    if (inventory_year == "2025"):
       label_name = 'High impact'
    else:
       label_name = 'Rights/safety-impacting'
    legend_patches = [
        mpatches.Patch(color='#378ADD', label='All use cases'),
        mpatches.Patch(color='#D85A30', label=label_name)
    ]
    ax.legend(handles=legend_patches, fontsize=10, loc='lower right',
              frameon=True, framealpha=0.9)
  
  #plt.tight_layout()
  translator = str.maketrans("", "", string.punctuation)
  clean_text = topic_name.translate(translator)
  output_dir = Path('./' + clean_text.lower().replace(" ", "_"))
  fig_name = data_subset.lower().replace(" ", "_") + '_' + inventory_year + '.png'
  file_path = output_dir / fig_name
  output_dir.mkdir(parents=True, exist_ok=True)
  plt.savefig(file_path, dpi=150, bbox_inches='tight')


"""Identify common use cases across 2023 and 2024 inventories.
This section processes the 2023 and 2024 AI use case inventories to find common use cases
based on their titles and departments, and also identifies potential duplicates within each year's inventory.
"""

inventory_2023["Title"] = inventory_2023["Title"].str.strip()
inventory_2023["Department"] = inventory_2023["Department"].str.strip()
inventory_2023["Agency"] = inventory_2023["Agency"].str.strip()
inventory_2024["Use Case Name"] = inventory_2024["Use Case Name"].str.strip()
inventory_2024["Agency"] = inventory_2024["Agency"].str.strip()
inventory_2024["Bureau"] = inventory_2024["Bureau"].str.strip()

common_use_cases = []
names_2023 = inventory_2023["Title"]
departments_2023 = inventory_2023["Department"]
names_departments_2023 = [name + "," + department for name, department in zip(names_2023, departments_2023)]

names_2024 = inventory_2024["Use Case Name"]
departments_2024 = inventory_2024["Agency"]
names_departments_2024 = [name + "," + department for name, department in zip(names_2024, departments_2024)]

# TODO: remove unnecessary concatenation

# Remove duplicate name x department pairs from names_2023
set_names_departments_2023 = list(set(names_departments_2023))

# Identify common use cases across 2023 and 2024 inventories
set_names_departments_2024 = set(names_departments_2024)
common_use_cases = [item for item in set_names_departments_2023 if item in set_names_departments_2024]

# How many duplicate name x department pairs are there in 2023?
all_2023_counts = pd.Series(names_departments_2023).value_counts()
duplicate_names_departments_2023 = all_2023_counts[all_2023_counts > 1].to_dict()
common_duplicate_names_departments_2023 = {k: v for k, v in duplicate_names_departments_2023.items() if k in common_use_cases}

# How many duplicate name x department pairs are there in 2024?
all_2024_counts = pd.Series(names_departments_2024).value_counts()
duplicate_names_departments_2024 = all_2024_counts[all_2024_counts > 1].to_dict()
common_duplicate_names_departments_2024 = {k: v for k, v in duplicate_names_departments_2024.items() if k in common_use_cases}


for key, value in common_duplicate_names_departments_2023.items():
  print(f"2023 Key: {key}, 2023 Value: {value}")

for key, value in common_duplicate_names_departments_2024.items():
  print(f"2024 Key: {key}, 2024 Value: {value}")

common_use_cases_names = [i.split(",")[0] for i in common_use_cases]
common_use_cases_departments = [i.split(",")[1] for i in common_use_cases]


"""Determine whether 2024 use cases with identical names are actually duplicates, where names are restricted to the common set of names across 2023 and 2024 inventories."""

# The 2024 use cases are actually unique although their names overlap
duplicate_names_departments_2024_list = list(duplicate_names_departments_2024.keys())
duplicate_names = [i.split(",")[0] for i in duplicate_names_departments_2024_list]
duplicate_departments = [i.split(",")[1] for i in duplicate_names_departments_2024_list]

duplicate_use_cases_2024 = inventory_2024[(inventory_2024["Use Case Name"].isin(duplicate_names)) &
                                          (inventory_2024["Agency"].isin(duplicate_departments))]
duplicate_use_cases_2024.to_excel("duplicate_use_cases_2024.xlsx", index=False)

"""Compare metadata of the above 2024 use cases to metadata of 2023 use cases that have identical names and departments to determine which 2024 use cases map to 2023 use cases."""

# A manual comparison of both spreadsheets shows that the 2024 website chatbot use case with the purpose "The chatbot helps the end user with basic information about the Workforce Recruitment Program ..."
# and the 2024 chatbot use case with the purpose "For the Patient Safety Organization Privacy Protection Center website ..." have no 2023 counterparts
duplicate_use_cases_2023 = inventory_2023[(inventory_2023["Title"].isin(duplicate_names)) &
                                          (inventory_2023["Department"].isin(duplicate_departments))]
duplicate_use_cases_2023.to_excel("duplicate_use_cases_2023.xlsx", index=False)

"""Compare development stages and other metadata of common, de-duplicated use cases in 2023 and 2024

TODO: check to make sure that summaries and agencies in filtered_inventory_2023 map to those in filtered_inventory_2024
"""

filtered_inventory_2023 = inventory_2023[(inventory_2023["Title"].isin(common_use_cases_names)) &
                                         (inventory_2023["Department"].isin(common_use_cases_departments))]
# Remove two 2024 use cases that lack a 2023 counterpart
filtered_inventory_2024 = inventory_2024[(inventory_2024["Use Case Name"].isin(common_use_cases_names)) &
                                         (inventory_2024["Agency"].isin(common_use_cases_departments)) &
                                         ~(inventory_2024["What is the intended purpose and expected benefits of the AI?"].str.contains("The chatbot helps the end user with basic information about the Workforce Recruitment Program", na=False)) &
                                         ~(inventory_2024["What is the intended purpose and expected benefits of the AI?"].str.contains("For the Patient Safety Organization Privacy Protection Center website", na=False))]

# print(len(filtered_inventory_2023))
# print(len(filtered_inventory_2024))

# Record development stages of common use cases in 2023 and 2024 and save to spreadsheet
development_stages_2024 = []
agencies_2024 = []
summaries_2024 = []

filtered_names_2023 = filtered_inventory_2023["Title"]
filtered_departments_2023 = filtered_inventory_2023["Department"]
filtered_names_departments_2023 = [name + "," + department for name, department in zip(filtered_names_2023, filtered_departments_2023)]

filtered_names_2024 = filtered_inventory_2024["Use Case Name"]
filtered_departments_2024 = filtered_inventory_2024["Agency"]
filtered_names_departments_2024 = [name + "," + department for name, department in zip(filtered_names_2024, filtered_departments_2024)]
filtered_inventory_dev_2024_dict = dict(zip(filtered_names_departments_2024, filtered_inventory_2024["Stage of Development"]))
filtered_inventory_agency_2024_dict = dict(zip(filtered_names_departments_2024, filtered_inventory_2024["Bureau"]))
filtered_inventory_summary_2024_dict = dict(zip(filtered_names_departments_2024, filtered_inventory_2024["What is the intended purpose and expected benefits of the AI?"]))

for name_dept in filtered_names_departments_2023:
  development_stages_2024.append(filtered_inventory_dev_2024_dict[name_dept])

for name_dept in filtered_names_departments_2023:
  agencies_2024.append(filtered_inventory_agency_2024_dict[name_dept])

for name_dept in filtered_names_departments_2023:
  summaries_2024.append(filtered_inventory_summary_2024_dict[name_dept])

development_stages_2023_2024 = filtered_inventory_2023[["Title", "Department", "Summary", "Agency", "Development_Stage"]].copy()
development_stages_2023_2024.rename(columns={"Development_Stage": "Development_Stage_2023", "Summary" : "Summary_2023", "Agency" : "Agency_2023"}, inplace=True)
development_stages_2023_2024["Development_Stage_2024"] = development_stages_2024
development_stages_2023_2024["Agency_2024"] = agencies_2024
development_stages_2023_2024["Summary_2024"] = summaries_2024

# Move Agency_2024 and Summary_2024 next to their 2023 counterparts
cols = development_stages_2023_2024.columns.tolist()
new_cols_summary = cols[:3] + [cols[-1]] + cols[3:-1]

# Columns are now title, department, summary_2023, summary_2024, agency_2023, dev_stage_2023, dev_stage_2024, agency_2024
new_cols_agency = new_cols_summary[:5] + [new_cols_summary[-1]] + new_cols_summary[5:-1]
development_stages_2023_2024 = development_stages_2023_2024[new_cols_agency]
development_stages_2023_2024.to_excel("dev_stages_2023_2024.xlsx", index=False)

"""TODO: Analyze changes in development stages

Group 2023, 2024, and 2025 inventories by agency and bureau and visualize application areas for these groupings

Group dataframes just by agency and by agency and bureau
"""

grouped_department_2023 = inventory_2023.groupby(["Department"])
grouped_department_2024 = inventory_2024.groupby(["Agency"])
grouped_department_2025 = inventory_2025.groupby(["Agency Name"])
grouped_department_agency_2023 = inventory_2023.groupby(["Department", "Agency"])
grouped_department_agency_2024 = inventory_2024.groupby(["Agency", "Bureau"])
grouped_department_agency_2025 = inventory_2025.groupby(["Agency Name", "Bureau/Component"])

"""Sort groups in descending order based on their size"""

sorted_groups_department_2023 = grouped_department_2023.size().sort_values(ascending=False)
sorted_groups_department_2024 = grouped_department_2024.size().sort_values(ascending=False)
sorted_groups_department_2025 = grouped_department_2025.size().sort_values(ascending=False)
sorted_groups_department_agency_2023 = grouped_department_agency_2023.size().sort_values(ascending=False)
sorted_groups_department_agency_2024 = grouped_department_agency_2024.size().sort_values(ascending=False)
sorted_groups_department_agency_2025 = grouped_department_agency_2025.size().sort_values(ascending=False)


"""Print out agencies and bureaus in descending order based on the number of use cases"""

sorted_grouped_depts = [sorted_groups_department_2023, sorted_groups_department_2024, sorted_groups_department_2025]
sorted_grouped_depts_agencies = [sorted_groups_department_agency_2023, sorted_groups_department_agency_2024, sorted_groups_department_agency_2025]
grouped_dfs = []

for i in range(0, len(sorted_grouped_depts)):
  sorted_group_dept = sorted_grouped_depts[i]
  group_df = pd.DataFrame({
      "Department": sorted_group_dept.index,
      "Number of use cases": sorted_group_dept.values
  })
  grouped_dfs.append(group_df)

for i in range(0, len(sorted_grouped_depts_agencies)):
  sorted_group_dept_agency = sorted_grouped_depts_agencies[i]
  department_name = [idx[0] for idx in sorted_group_dept_agency.index]
  agency_name = [idx[1] for idx in sorted_group_dept_agency.index]
  group_df = pd.DataFrame({
      "Department": department_name,
      "Agency": agency_name,
      "Number of use cases": sorted_group_dept_agency.values
  })
  grouped_dfs.append(group_df)


with pd.ExcelWriter("groups_department_agency_2023_2024_2025.xlsx") as writer:
    grouped_dfs[0].to_excel(writer, sheet_name="grouped_department_2023", index=False)
    grouped_dfs[1].to_excel(writer, sheet_name="grouped_department_2024", index=False)
    grouped_dfs[2].to_excel(writer, sheet_name="grouped_department_2025", index=False)
    grouped_dfs[3].to_excel(writer, sheet_name="grouped_department_agency_2023", index=False)
    grouped_dfs[4].to_excel(writer, sheet_name="grouped_department_agency_2024", index=False)
    grouped_dfs[5].to_excel(writer, sheet_name="grouped_department_agency_2025", index=False)

"""Display 2024 use case topic areas and rights/safety-impacting designations for top five agencies"""

for i in sorted_groups_department_2024.index[:5]:
  use_case_topic = grouped_department_2024.get_group((i,))["Use Case Topic Area"]
  use_case_rights = grouped_department_2024.get_group((i,))[["Is the AI use case rights-impacting, safety-impacting, both, or neither?", "Use Case Topic Area"]]
  use_case_rights = use_case_rights[use_case_rights["Is the AI use case rights-impacting, safety-impacting, both, or neither?"].str.lower().isin(["both", "case-by-case assessment", "rights-impacting", "safety-impacting"])]
  topic_rights = use_case_rights["Use Case Topic Area"].value_counts()
  
  topic_counts = use_case_topic.value_counts()
  topics = topic_counts.index.tolist()
  totals = topic_counts.values.tolist()
  rights_counts = [topic_rights.get(t, 0) for t in topics]

  create_plot(topics, totals, "Use Case Topic Area", str(i), "2024", rights_counts)

"""Display fields for entire 2024 inventory and rights/safety-impacting designations"""
cols = inventory_2024.columns
fields = [cols[4], cols[9:11].tolist(), cols[15], cols[17], cols[19:21].tolist(), cols[22:25].tolist(), cols[27:29].tolist(), cols[30:32].tolist(), cols[33], 
                 cols[35:37].tolist(), cols[38], cols[40], cols[42:47].tolist(), cols[48:51].tolist(), cols[52], cols[54], cols[56], cols[58], cols[60]]

flat_list = []
for item in fields:
    if isinstance(item, list):
        flat_list.extend(item)  # Unpacks the sublist elements
    else:
        flat_list.append(item)  # Appends the standalone number

#print(flat_list)
for field in flat_list:
  field_counts = inventory_2024[field].value_counts()
  fields = field_counts.index.tolist()
  totals = field_counts.values.tolist()

  if (field.startswith("Is the AI use case rights-impacting") == False):
    use_case_rights = inventory_2024[["Is the AI use case rights-impacting, safety-impacting, both, or neither?", field]]
    use_case_rights = use_case_rights[use_case_rights["Is the AI use case rights-impacting, safety-impacting, both, or neither?"].str.lower().isin(["both", "case-by-case assessment", "rights-impacting", "safety-impacting"])]
    field_rights = use_case_rights[field].value_counts()
    hi_counts = [field_rights.get(f, 0) for f in fields]
    create_plot(fields, totals, field, "Full Inventory",  "2024", hi_counts)
  else:
     create_plot(fields, totals, field, "Full Inventory",  "2024")


"""Display 2025 use case topic areas and high-impact designations for top five agencies"""

for i in sorted_groups_department_2025.index[:5]:

  use_case_topic = grouped_department_2025.get_group((i,))["Use Case Topic Area"]
  use_case_hi = grouped_department_2025.get_group((i,))[["Is the AI use case high-impact?", "Use Case Topic Area"]]
  use_case_hi = use_case_hi[use_case_hi["Is the AI use case high-impact?"].str.lower().isin(["a) high-impact", "b) presumed high-impact, but determined not high impact"])]
  topic_hi = use_case_hi["Use Case Topic Area"].value_counts()
  
  topic_counts = use_case_topic.value_counts()
  topics = topic_counts.index.tolist()
  totals = topic_counts.values.tolist()
  hi_counts = [topic_hi.get(t, 0) for t in topics]

  create_plot(topics, totals, "Use Case Topic Area", str(i), "2025", hi_counts)
