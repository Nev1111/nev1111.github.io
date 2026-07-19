---
name: multi-year-consolidation
title: Consolidate Multi-Year Files into One Dataset
description: Stack yearly Excel/CSV extracts with inconsistent column names into one consolidated DataFrame using pd.concat, with a source-file column and column normalization so every row is traceable and totals tie to the originals.
category: summarization
tools: pandas
---

## When to use this skill

- You've been asked for a trend across 3, 5, or 10 years, and each year lives in its own file (`Holdings_2022.xlsx`, `Holdings_2023_FINAL.xlsx`, ...).
- Column names drift between years — `CUSIP` vs `Security ID` vs `Security_ID`, `Market Value` vs `Fair Value` — so a naive copy-paste misaligns data.
- You want a consolidation you can rerun next year, with an audit trail showing exactly which file each row came from.

The pattern: read each file, tag it with its year and source filename, normalize column names to one standard, then `pd.concat` everything into a single tall dataset.

## Inputs it expects

- One file per year (Excel or CSV), each containing the same *kind* of data at the same level of detail (e.g., one row per security).
- A way to know each file's year — from the filename or a date column inside the file.
- A mapping of known column-name variants to your standard names. Build this by eyeballing each file's headers first; don't guess.
- Agreement on which columns are required (identifier, amount, date) so you can check every year supplied them.

## Steps

1. Read each year's file and print its row count and column list — this is your per-file control total, write it down.
2. Normalize column names with a rename mapping so every year uses identical standard names.
3. Add `Fiscal_Year` and `Source_File` columns to each frame before combining — once stacked, these are the only way to trace a row home.
4. Combine with `pd.concat(dfs, ignore_index=True)`. Then check for columns that exist in only some years — `concat` aligns by name and fills the gaps with `NaN` rather than erroring.
5. Run the control totals, then check for cross-year duplicates before summarizing.

## Code

```python
import pandas as pd

# Map each year's column-name quirks to one standard
COLUMN_MAPPING = {
    'CUSIP': 'Security_ID', 'Security ID': 'Security_ID', 'SecID': 'Security_ID',
    'Market Value': 'Market_Value', 'Fair Value': 'Market_Value', 'MktValue': 'Market_Value',
    'As of Date': 'Report_Date', 'AsOfDate': 'Report_Date', 'Date': 'Report_Date',
}

files = {
    2022: 'Holdings_2022.xlsx',
    2023: 'Holdings_2023_FINAL.xlsx',
    2024: 'Holdings_2024.xlsx',
}

dfs = []
file_counts = {}   # per-file control totals, captured at load time

for year, filename in files.items():
    df = pd.read_excel(filename)
    df = df.rename(columns=COLUMN_MAPPING)

    # Traceability: every row keeps its year and source file
    df['Fiscal_Year'] = year
    df['Source_File'] = filename

    file_counts[filename] = {'rows': len(df), 'total_value': df['Market_Value'].sum()}
    dfs.append(df)
    print(f"Loaded {year}: {len(df):,} rows, {df['Market_Value'].sum():,.2f} from {filename}")

# Stack all years; concat aligns by column name and fills gaps with NaN
combined = pd.concat(dfs, ignore_index=True)

# Columns not present in every year show up as partial NaN — list them
sparse_cols = combined.columns[combined.isna().any()].tolist()
print(f"\nConsolidated: {len(combined):,} rows, "
      f"{combined['Fiscal_Year'].min()}-{combined['Fiscal_Year'].max()}")
if sparse_cols:
    print(f"Columns missing in some years: {sparse_cols}")

# Year-over-year summary from the consolidated data
yoy = combined.groupby('Fiscal_Year')['Market_Value'].sum()
print(yoy)
```

## Validation (control totals)

- **Row counts add up:** `len(combined)` must equal the sum of every per-file row count captured at load time. Any difference means a file was dropped or double-loaded.
- **Grand total ties:** `combined['Market_Value'].sum()` must equal the sum of the per-file `total_value` figures, and each year's slice (`combined[combined['Fiscal_Year'] == y]['Market_Value'].sum()`) must match that file's original total to the penny.
- **Every row is traceable:** `combined['Source_File'].isna().sum()` and `combined['Fiscal_Year'].isna().sum()` are both 0.
- **File coverage:** `combined['Source_File'].nunique()` equals the number of files you intended to load — catches a silently skipped year.
- **Duplicate check:** `combined.duplicated(subset=['Security_ID', 'Fiscal_Year']).sum()` should be 0 if each file has one row per security.

## Exceptions to surface

- Rows with `NaN` in a required column after concat — usually a column-name variant the mapping didn't cover, so a whole year's values landed in an unmapped column. Show the affected `Source_File`.
- Duplicate (Security_ID, Fiscal_Year) pairs — the same holding loaded twice, or a "v2" file overlapping a "FINAL" file.
- Files that matched the folder pattern but failed to load, or years with zero rows — the reviewer must confirm whether the year genuinely had no activity.
- Identifiers that appear in one year but vanish the next (or appear from nowhere) — legitimate buys/sells or a sign the identifier format changed between systems.
- A year whose row count or total value swings sharply from its neighbors (e.g., half the rows of every other year) — often a partial extract rather than a real trend.
