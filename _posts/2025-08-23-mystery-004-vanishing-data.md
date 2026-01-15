---
layout: mystery
title: "The Case of the Vanishing Data"
mystery_number: 004
series: "Masha & Panda Mysteries"
difficulty_level: "beginner"
estimated_time: "8 minutes"
skills_covered: [missing_data, data_quality, isna_function]
real_scenario: true
character_focus: "both"
date: 2025-08-23
categories: [mysteries, data-quality]
tags: [pandas, missing-data, data-validation, isna]
previous_mystery: "/2025-08-23-mystery-003-time-traveling-addresses/"
next_mystery: "/2025-08-23-mystery-005-buried-treasure/"
---

## The Case

The monthly financial report was due in two hours, but Sarah had a sinking feeling as she stared at her screen. The imported data looked complete at first glance - thousands of rows of transactions, customer names, amounts, dates. But something was wrong with the totals.

"The revenue summary doesn't match the detail," she muttered, double-checking her Excel formulas. "According to this, we should have $2.3 million in sales, but the detail only adds up to $1.8 million. Where did half a million dollars disappear to?"

> **Masha**: "I hate when this happens! The data looks fine when you scroll through it, but somewhere in those thousands of rows, there are invisible blanks messing up our calculations. How are we supposed to find empty cells in a dataset this big?"

Sarah started scrolling through the data manually, looking for obviously blank cells. Row 847 looked fine. Row 1,205 had all the values filled in. Row 1,847 seemed complete too. But she knew that somewhere in this mass of data, there were missing values causing the revenue calculations to fail.

The clock was ticking. In two hours, the CFO would be expecting the monthly numbers, and Sarah couldn't deliver a report when she couldn't trust the data quality.

> **Panda**: "You know, Masha, instead of hunting for invisible needles in this haystack, we can get pandas to be our detective. It can instantly find every single row that has missing data, no matter how well hidden those blank cells are."

Sarah realized this wasn't just about today's report. Every month, they imported data from multiple systems, and there were always data quality issues hiding in the details. Customer names that didn't load, amounts that came through as blank, dates that failed to import properly.

> **Masha**: "So instead of playing hide-and-seek with missing data, we can just ask pandas to show us every single row that has any blank spots? That would save us hours of detective work!"
> 
> **Panda**: "Exactly! The `isna()` function can peek into every cell and identify the culprits. Then we can decide whether to fix them, exclude them, or fill them with default values. No more mystery math in our reports."

Within minutes, Sarah had identified 127 rows with missing data - some had blank customer names, others had missing amounts, and a few were missing transaction dates entirely. Once she knew exactly which records were problematic, she could make informed decisions about how to handle them for the report.

## The Solution

Here's how to quickly identify and handle missing data in your datasets:

```python
import pandas as pd
import numpy as np

# Sample data with missing values (represented as NaN)
df = pd.DataFrame({
 'Customer_ID': [1001, 1002, np.nan, 1004, 1005, 1006],
 'Customer_Name': ['ABC Corp', 'XYZ Ltd', 'DEF Inc', np.nan, 'GHI Co', 'JKL Corp'],
 'Amount': [15000, np.nan, 8500, 12000, np.nan, 22000],
 'Date': ['2023-01-15', '2023-01-16', np.nan, '2023-01-18', '2023-01-19', '2023-01-20']
})

print("Original Dataset:")
print(df)
print()

# Step 1: Get a quick overview of missing data
print("Missing data overview:")
print("Total missing values per column:")
print(df.isna().sum())
print()

print("Percentage missing per column:")
print((df.isna().sum() / len(df) * 100).round(1))
print()

# Step 2: Find rows with ANY missing data
rows_with_missing = df[df.isna().any(axis=1)]
print("Rows with any missing data:")
print(rows_with_missing)
print()

print(f"Found {len(rows_with_missing)} rows with missing data out of {len(df)} total rows")
print()

# Step 3: Find rows with missing data in specific columns
print("Rows missing Customer_ID:")
print(df[df['Customer_ID'].isna()])
print()

print("Rows missing Amount:")
print(df[df['Amount'].isna()])
print()

# Step 4: Find COMPLETE rows (no missing data)
complete_rows = df[df.notna().all(axis=1)]
print("Complete rows (no missing data):")
print(complete_rows)
print()

# Step 5: Create a data quality report
quality_report = pd.DataFrame({
 'Column': df.columns,
 'Total_Values': len(df),
 'Missing_Count': df.isna().sum().values,
 'Missing_Percent': (df.isna().sum().values / len(df) * 100).round(1),
 'Complete_Count': df.notna().sum().values
})

print("Data Quality Report:")
print(quality_report.to_string(index=False))
print()

# Step 6: Show different handling strategies
print("Strategy 1 - Remove rows with ANY missing data:")
clean_df = df.dropna()
print(f"Original: {len(df)} rows → Clean: {len(clean_df)} rows")
print()

print("Strategy 2 - Remove rows missing critical columns (Customer_ID or Amount):")
critical_complete = df.dropna(subset=['Customer_ID', 'Amount'])
print(f"Original: {len(df)} rows → Critical Complete: {len(critical_complete)} rows")
print()

print("Strategy 3 - Fill missing values:")
filled_df = df.copy()
filled_df['Customer_Name'] = filled_df['Customer_Name'].fillna('Unknown Customer')
filled_df['Amount'] = filled_df['Amount'].fillna(0)
print("After filling missing values:")
print(filled_df)
```

## Key Learning Points

- **isna() reveals invisible problems**: Missing data often hides in large datasets, causing calculation errors and report discrepancies
- **any(axis=1) finds problematic rows**: Use this to identify any row that has at least one missing value across all columns
- **Data quality should be checked first**: Always assess missing data before performing calculations or analysis
- **Multiple strategies for handling missing data**: Drop rows, fill with defaults, or focus on critical columns only
- **Create systematic quality reports**: Track missing data patterns to identify recurring import issues
- **Prevention is better than detection**: Work with data providers to improve source data quality over time

---

*Ready for your next mystery? Check out the [Masha & Panda Mystery Series](/mysteries) for more accounting adventures!*