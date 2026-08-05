# Federal AI Use Case Inventory Analysis

A Python script for analyzing and comparing Federal AI Use Case Inventories across 2023, 2024, and 2025. It loads and cleans inventory data, identifies common and duplicate use cases across years, generates comparative visualizations, and exports findings to Excel reports.

---

## Features

- **Multi-year data loading** — Reads 2023, 2024, and 2025 Federal AI Use Case Inventory files from local Excel/XLS files
- **Data cleaning** — Strips whitespace from all string values and column names across all inventories; normalizes string `"N/A"` and `"NA"` values to `"Not Applicable"` and fills remaining empty cells with `"None"` (rather than leaving them as `NaN`)
- **Cross-year comparison** — Identifies use cases that appear in both the 2023 and 2024 inventories by matching on title and department/agency
- **Duplicate detection** — Flags potential duplicate use cases within each year's inventory
- **Development stage tracking** — Compares the development stage of common use cases between 2023 and 2024
- **Agency/bureau grouping** — Groups use cases by department and agency/bureau across all three years, sorted by volume
- **Visualization** — Generates horizontal bar charts of use case topic areas by agency, with overlaid counts for rights/safety-impacting (2024) or high-impact (2025) designations
- **Excel export** — Saves multiple analytical outputs as `.xlsx` files

---

## Requirements

Install dependencies via pip:

```bash
pip install pandas matplotlib numpy seaborn openpyxl xlrd
```

| Package | Purpose |
|---|---|
| `pandas` | Data loading, cleaning, grouping, and export |
| `matplotlib` | Bar chart generation |
| `numpy` | Array operations for chart layout |
| `seaborn` | Imported (available for styling) |
| `openpyxl` | Writing `.xlsx` files |
| `xlrd` | Reading legacy `.xls` files (2024 inventory) |

---

## Input Files

Place the following files in an `./inventories/` directory relative to the script:

| File | Source |
|---|---|
| `2023_consolidated_ai_inventory_raw.xlsx` | [ombegov/2024-Federal-AI-Use-Case-Inventory](https://github.com/ombegov/2024-Federal-AI-Use-Case-Inventory/blob/main/data/2023_consolidated_ai_inventory_raw.csv) (converted to Excel) |
| `2024_consolidated_ai_inventory_raw_v2.xls` | [ombegov/2024-Federal-AI-Use-Case-Inventory](https://github.com/ombegov/2024-Federal-AI-Use-Case-Inventory/blob/main/data/2024_consolidated_ai_inventory_raw_v2.xls) |
| `2025_individually_reported_AI_use_cases.xlsx` | [ombegov/2025-Federal-Agency-AI-Use-Case-Inventory](https://github.com/ombegov/2025-Federal-Agency-AI-Use-Case-Inventory/blob/main/Data/2025_individually_reported_AI_use_cases.xlsx) |

---

## Usage

```bash
python ai_inventory_11_03_25.py
```

The script runs sequentially through all analysis steps and writes outputs to the working directory.

---

## Outputs

### Excel Files

| File | Contents |
|---|---|
| `duplicate_use_cases_2023.xlsx` | 2023 use cases with duplicate name × department pairs |
| `duplicate_use_cases_2024.xlsx` | 2024 use cases with duplicate name × department pairs |
| `dev_stages_2023_2024.xlsx` | Side-by-side comparison of common use cases across 2023 and 2024, including title, department, summary (both years), agency/bureau (both years), and development stage (both years) |
| `groups_department_agency_2023_2024_2025.xlsx` | Six-sheet workbook with use case counts grouped by department and by department × agency for each year |

### Chart Images

Bar charts are saved as `.png` files (150 DPI) under `./data/`, in subdirectories named after the topic field (e.g., `./data/use_case_topic_area/`). Excel files are written to the working directory (where the script is run from). Charts are generated for:

- The top 5 agencies in the 2024 inventory — topic area breakdown with rights/safety-impacting overlay
- The full 2024 inventory — a broad set of fields (topic area, development stage, rights/safety impact designation, and many others) each plotted with a rights/safety-impacting overlay where applicable
- The top 5 agencies in the 2025 inventory — topic area breakdown with high-impact overlay

---

## Key Functions

### `create_plot(topic_indices, topic_values, topic_name, data_subset, inventory_year, sub_topic_counts=None)`

Generates and saves a horizontal bar chart.

| Parameter | Type | Description |
|---|---|---|
| `topic_indices` | list | Y-axis labels (topic names) |
| `topic_values` | list | Total use case counts per topic |
| `topic_name` | str | Field being plotted (used in title and output directory name) |
| `data_subset` | str | Description of the data slice (e.g., agency name or `"Full Inventory"`) |
| `inventory_year` | str | Year of the inventory (`"2023"`, `"2024"`, or `"2025"`) |
| `sub_topic_counts` | list, optional | Counts for a sub-category (rights/safety-impacting or high-impact) overlaid as a second bar |

---

## Known Limitations & TODOs

- Two 2024 use cases are manually excluded from cross-year comparison because they lack 2023 counterparts (identified by inspecting purpose text). This logic is hardcoded and may need revisiting if source data changes.
- A TODO notes unnecessary string concatenation in the cross-year matching logic that can be simplified.
- Analysis of development stage *changes* between 2023 and 2024 is not yet implemented (marked TODO).
- Validation that summaries and agencies in the filtered 2023 inventory correctly map to their 2024 counterparts is noted as a TODO.

---

## Data Notes

The 2023 and 2024 inventories use different column naming conventions (e.g., `"Title"` vs. `"Use Case Name"`, `"Department"` vs. `"Agency"`). The script accounts for these differences throughout. The 2025 inventory introduces an `"Is the AI use case high-impact?"` field in place of the 2024 rights/safety-impacting field.
