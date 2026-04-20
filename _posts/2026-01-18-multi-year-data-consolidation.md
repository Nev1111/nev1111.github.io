---
layout: post
title: "Multi-Year Data Consolidation: From Chaos to Clarity"
subtitle: "Combine 5+ years of data from different Excel files with inconsistent formats. Python makes it effortless."
tags: [python, pandas, data-consolidation, multi-year-analysis, excel, automation]
comments: true
author: PANDAUDIT Team
---

## The Multi-Year Analysis Problem

Your boss asks: *"Can you show me investment performance trends for the last 5 years?"*

You know what comes next:

1. **Hunt for files:** `Holdings_2020.xlsx`, `Holdings_2021_FINAL.xlsx`, `Holdings2022.xlsx` (no underscore?), `2023_Holdings_v2.xlsx`...
2. **Open each file:** Column names slightly different in each
3. **Copy-paste into master:** Pray you don't miss anything
4. **Fix formatting:** Different date formats, inconsistent column order
5. **4 hours later:** Finally have consolidated data... but is it right?

**There's a better way.** Let Python do this in 30 seconds.

---

## The Challenge: Inconsistent Multi-Year Data

### What Makes This Hard:

**File naming inconsistencies:**
```
Holdings_2020.xlsx
Holdings_2021_Final.xlsx 
2022_Holdings.xlsx (year at beginning?)
holdings_2023.xlsx (lowercase?)
Holdings 2024.xlsx (space instead of underscore?)
```

**Column naming variations:**
```
2020: "Security ID" | "Market Value" | "Date"
2021: "CUSIP" | "Fair Value" | "As of Date"
2022: "Security_ID" | "MktValue" | "Date"
```

**Sheet name changes:**
```
2020: Sheet = "Holdings"
2021: Sheet = "Portfolio"
2022: Sheet = "Sheet1"
```

Excel makes you handle each manually. Python handles this programmatically.

---

## Solution 1: Basic Multi-Year Consolidation

### When Files Are Reasonably Consistent

```python
import pandas as pd

# Define years to consolidate
years = [2020, 2021, 2022, 2023, 2024]

# List to store each year's data
dfs = []

for year in years:
 # Read the file
 filename = f'Holdings_{year}.xlsx'
 df = pd.read_excel(filename)
 
 # Add year column
 df['Year'] = year
 
 # Append to list
 dfs.append(df)
 print(f" Loaded {year}: {len(df):,} rows")

# Combine all years into single DataFrame
combined = pd.concat(dfs, ignore_index=True)

print(f"\n Consolidated {len(combined):,} total rows across {len(years)} years")
print(f" Date range: {combined['Date'].min()} to {combined['Date'].max()}")

# Export
combined.to_excel('Holdings_2020_2024_Consolidated.xlsx', index=False)
```

**Output:**
```
 Loaded 2020: 1,247 rows
 Loaded 2021: 1,389 rows
 Loaded 2022: 1,512 rows
 Loaded 2023: 1,678 rows
 Loaded 2024: 1,801 rows

 Consolidated 7,627 total rows across 5 years
 Date range: 2020-01-01 to 2024-12-31
```

---

## Solution 2: Handle Inconsistent File Names

### When File Naming is a Mess

```python
import pandas as pd
import glob
import re

# Find all files matching pattern (flexible matching)
files = glob.glob('*[Hh]oldings*202[0-4]*.xlsx')
files.sort() # Ensure chronological order

print(f"Found {len(files)} files:")
for f in files:
 print(f" - {f}")

dfs = []

for file in files:
 # Extract year from filename using regex
 year_match = re.search(r'(202[0-4])', file)
 if year_match:
 year = int(year_match.group(1))
 else:
 print(f"Warning: Could not extract year from: {file}")
 continue
 
 # Read file
 df = pd.read_excel(file)
 df['Year'] = year
 df['Source_File'] = file # Track where data came from
 
 dfs.append(df)
 print(f" {year}: {len(df):,} rows from {file}")

# Combine
combined = pd.concat(dfs, ignore_index=True)

print(f"\n Consolidated {len(combined):,} rows")
```

---

## Solution 3: Handle Inconsistent Column Names

### Normalize Column Names Across Years

```python
import pandas as pd

def normalize_columns(df):
 """Standardize column names across different years"""
 
 # Create mapping dictionary (old name -> new name)
 column_mapping = {
 # Security identifier variations
 'CUSIP': 'Security_ID',
 'Security ID': 'Security_ID',
 'SecID': 'Security_ID',
 'Cusip': 'Security_ID',
 
 # Market value variations
 'Market Value': 'Market_Value',
 'Fair Value': 'Market_Value',
 'MktValue': 'Market_Value',
 'FairValue': 'Market_Value',
 'Value': 'Market_Value',
 
 # Date variations
 'As of Date': 'Date',
 'AsOfDate': 'Date',
 'Report Date': 'Date',
 'ReportDate': 'Date'
 }
 
 # Rename columns
 df = df.rename(columns=column_mapping)
 
 return df

# Apply to multi-year consolidation
dfs = []
for year in [2020, 2021, 2022, 2023, 2024]:
 df = pd.read_excel(f'Holdings_{year}.xlsx')
 df['Year'] = year
 
 # Normalize column names
 df = normalize_columns(df)
 
 dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)

print("Standardized columns:")
print(combined.columns.tolist())
```

---

## Solution 4: Handle Different Sheet Names

### When Each Year Uses Different Sheet Names

```python
import pandas as pd

def read_holdings_file(filename, year):
 """
 Read holdings file, handling different sheet names
 """
 
 # Try common sheet names in order of likelihood
 sheet_names_to_try = ['Holdings', 'Portfolio', 'Data', 'Sheet1', 0]
 
 for sheet_name in sheet_names_to_try:
 try:
 df = pd.read_excel(filename, sheet_name=sheet_name)
 print(f" {year}: Read from sheet '{sheet_name}'")
 return df
 except:
 continue
 
 # If all failed
 raise ValueError(f"Could not find data in {filename}")

# Usage in consolidation
dfs = []
for year in [2020, 2021, 2022, 2023, 2024]:
 filename = f'Holdings_{year}.xlsx'
 df = read_holdings_file(filename, year)
 df['Year'] = year
 dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)
```

---

## Solution 5: Complete Production-Ready Consolidation

### Handle All Edge Cases

```python
import pandas as pd
import glob
import re
from datetime import datetime

def consolidate_multi_year_data(
 file_pattern='*Holdings*202*.xlsx',
 output_file='Consolidated_Holdings.xlsx'
):
 """
 Consolidate multiple years of data files with error handling
 
 Args:
 file_pattern: glob pattern to match files
 output_file: name for consolidated output
 
 Returns:
 Consolidated DataFrame
 """
 
 # Find all matching files
 files = glob.glob(file_pattern)
 files.sort()
 
 if len(files) == 0:
 raise FileNotFoundError(f"No files found matching pattern: {file_pattern}")
 
 print(f" Found {len(files)} files to consolidate:")
 for f in files:
 print(f" - {f}")
 
 dfs = []
 errors = []
 
 for file in files:
 try:
 # Extract year
 year_match = re.search(r'(20\d{2})', file)
 year = int(year_match.group(1)) if year_match else None
 
 # Try to read file
 df = None
 for sheet_name in ['Holdings', 'Portfolio', 'Data', 0]:
 try:
 df = pd.read_excel(file, sheet_name=sheet_name)
 break
 except:
 continue
 
 if df is None:
 raise ValueError(f"Could not read any sheet from {file}")
 
 # Add metadata
 df['Year'] = year
 df['Source_File'] = file
 df['Import_Date'] = datetime.now()
 
 # Normalize column names
 df = normalize_columns(df)
 
 dfs.append(df)
 print(f" {year}: {len(df):,} rows")
 
 except Exception as e:
 print(f" Error processing {file}: {str(e)}")
 errors.append((file, str(e)))
 continue
 
 if len(dfs) == 0:
 raise ValueError("No files were successfully processed!")
 
 # Combine all DataFrames
 combined = pd.concat(dfs, ignore_index=True)
 
 # Data quality checks
 print(f"\n Consolidation Summary:")
 print(f" Total rows: {len(combined):,}")
 print(f" Years: {combined['Year'].min()} - {combined['Year'].max()}")
 print(f" Date range: {combined['Date'].min()} to {combined['Date'].max()}")
 
 # Check for duplicates
 duplicates = combined.duplicated(subset=['Security_ID', 'Date', 'Year']).sum()
 if duplicates > 0:
 print(f" Warning: {duplicates:,} potential duplicates detected")
 
 # Check for missing values
 missing_summary = combined.isnull().sum()
 if missing_summary.sum() > 0:
 print(f"\nWarning: Missing values detected:")
 print(missing_summary[missing_summary > 0])
 
 # Export consolidated data
 combined.to_excel(output_file, index=False)
 print(f"\n Saved to: {output_file}")
 
 # Export error log if any
 if len(errors) > 0:
 error_df = pd.DataFrame(errors, columns=['File', 'Error'])
 error_df.to_excel('Consolidation_Errors.xlsx', index=False)
 print(f"Warning: {len(errors)} files had errors - see Consolidation_Errors.xlsx")
 
 return combined

# Usage:
combined_data = consolidate_multi_year_data(
 file_pattern='Holdings_20*.xlsx',
 output_file='Holdings_2020_2024_Complete.xlsx'
)
```

---

## Bonus: Year-Over-Year Analysis

### Once You Have Consolidated Data

```python
# Year-over-year comparison
yoy = combined.groupby('Year')['Market_Value'].sum()

print("Year-over-Year Total Holdings:")
print(yoy)

# Calculate year-over-year growth
yoy_growth = yoy.pct_change() * 100

print("\nYear-over-Year Growth:")
for year, growth in yoy_growth.items():
 if pd.notna(growth):
 print(f" {year}: {growth:+.1f}%")

# Export summary
summary = pd.DataFrame({
 'Year': yoy.index,
 'Total_Value': yoy.values,
 'YoY_Growth_Pct': yoy_growth.values
})
summary.to_excel('YoY_Summary.xlsx', index=False)
```

---

## Bonus: Identify Securities That Appeared/Disappeared

```python
# Which securities were held in all years?
security_years = combined.groupby('Security_ID')['Year'].nunique()
held_all_years = security_years[security_years == combined['Year'].nunique()]

print(f"\n Securities held in ALL {combined['Year'].nunique()} years: {len(held_all_years)}")

# Which securities are new this year?
current_year = combined['Year'].max()
previous_year = current_year - 1

current_holdings = set(combined[combined['Year'] == current_year]['Security_ID'])
previous_holdings = set(combined[combined['Year'] == previous_year]['Security_ID'])

new_securities = current_holdings - previous_holdings
sold_securities = previous_holdings - current_holdings

print(f"\n🆕 New securities in {current_year}: {len(new_securities)}")
print(f" Securities sold from {previous_year}: {len(sold_securities)}")

# Export lists
pd.DataFrame({'Security_ID': list(new_securities)}).to_excel('New_Securities.xlsx', index=False)
pd.DataFrame({'Security_ID': list(sold_securities)}).to_excel('Sold_Securities.xlsx', index=False)
```

---

## Time Savings Comparison

| Task | Manual (Excel) | Python Automated |
|------|----------------|------------------|
| Find and open 5 files | 10 minutes | 2 seconds |
| Normalize column names | 30 minutes | Automatic |
| Copy-paste data | 20 minutes | Automatic |
| Verify no duplicates | 15 minutes | Automatic |
| Calculate YoY growth | 20 minutes | 5 seconds |
| **Total** | **~90 minutes** | **~30 seconds** |

**Time saved:** 99.4% reduction! 

---

## Benefits

 **Consistency:** Same process every time 
 **Speed:** 90+ minutes → 30 seconds 
 **Quality:** Automatic duplicate detection 
 **Auditability:** Track source files 
 **Scalability:** Handle 10 years as easily as 2 years 
 **Reusable:** Run monthly/quarterly with one click

---

## Try It Yourself!

### Quick Start:

```python
import pandas as pd

# Create sample files for 3 years
for year in [2022, 2023, 2024]:
 df = pd.DataFrame({
 'Security_ID': ['ABC123', 'XYZ789'],
 'Market_Value': [10000 * year, 20000 * year],
 'Date': [f'{year}-12-31', f'{year}-12-31']
 })
 df.to_excel(f'Holdings_{year}.xlsx', index=False)

# Now consolidate them
dfs = []
for year in [2022, 2023, 2024]:
 df = pd.read_excel(f'Holdings_{year}.xlsx')
 df['Year'] = year
 dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)
print(combined)
```

---

## What's Next?

Now that you have multi-year data:
- **Create pivot analysis** → [Read this post](/2026-01-12-pivot-tables-on-steroids-multi-level-analysis-in-one-line)
- **Calculate fiscal quarters** → [Read this post](/2026-01-13-government-fiscal-year-calculations-made-easy)
- **Detect trends** → Stay tuned for time-series analysis post!

---

## Your Turn!

**What multi-year consolidation challenges do you face?** Share in the comments!

**Have a different file structure?** We can help adapt this approach!

---

**Tags:** #Python #Pandas #DataConsolidation #MultiYear #ExcelAutomation #TimeSeriesAnalysis

---

*Part of the "Data Integration & Quality" series. Consolidate with confidence!*
