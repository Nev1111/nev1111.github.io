---
layout: post
title: "End-to-End: From Legacy Text Report to Executive Dashboard"
subtitle: "Watch a complete real-world workflow transform messy trial balance data into multi-dimensional analysis in 2 minutes. All patterns combined."
tags: [python, pandas, workflow, automation, trial-balance, end-to-end, complete-example]
comments: true
author: PANDAUDIT Team
---

## The Complete Challenge

**Your boss drops this bomb:** *"I need the Q4 expense analysis by budget category, broken down by fiscal quarter and month, with accruals separated from cash expenses. Oh, and identify any new accounts that need classification. Can you have it by end of day?"*

**Your reaction:** 

**In Excel:** 4-5 hours of manual work 
**With this Python workflow:** **2 minutes** 

Let me show you how.

---

## The Messy Starting Point

You receive a trial balance export from your legacy accounting system. It looks like this:

```
TRIAL BALANCE REPORT - FISCAL YEAR 2024
Fund: Special Fund 520

Account: 1234567-12-500100 Personnel - Salaries
 07/15/2024 GJ CD 12345 15,234.56
 07/20/2024 GJ CR 67890 2,500.00-
 
Account: 1234567-12-500200 Operations - Supplies
 08/10/2024 AI ACCRUE 1,234.00
 09/15/2024 GJ GJ 45678 5,678.90
 
Account: 2345678-13-600100 New Unclassified Account
 10/05/2024 AP VENDOR 15,000.00
```

**Problems:**
- Account numbers and descriptions are headers (not on every row)
- Dates are scattered throughout
- Amounts use trailing dash for credits (`2,500.00-`)
- Mix of transaction types (GJ, AI, AP)
- Some accounts aren't in your classification library yet
- Need fiscal quarters (July-June year)

**Goal:** Convert this chaos into an executive-ready multi-dimensional analysis.

---

## The Complete Python Workflow

### Step 1: Import and Parse

```python
import pandas as pd
import numpy as np
import re
from datetime import datetime

# Read the messy text/Excel export
tb = pd.read_excel('trial_balance_fy2024.xlsx', header=None, names=['description'])

# Fill any NaN with spaces
tb['description'] = tb['description'].fillna(' ')

print(f" Loaded {len(tb):,} rows from trial balance")

# Extract structured data from unstructured text
# Pattern: 7 digits, dash, 2 digits, dash, 6 digits
tb[['Account_num', 'Account_desc']] = tb['description'].str.extract(
 r'(\d{7}\-\d{2}\-\d{6})\s+(.*)'
)

# Extract dates (MM/DD/YYYY format)
tb['Month'] = tb['description'].str.extract(r"([0-9]{2}\/[0-9]{2}\/[0-9]{4})")

# Forward fill headers down to detail rows
tb['Account_num'] = tb['Account_num'].ffill()
tb['Account_desc'] = tb['Account_desc'].ffill()
tb['Month'] = tb['Month'].ffill()

print(f" Step 1: Parsed account numbers and dates")
```

---

### Step 2: Filter Transaction Types

```python
# Keep only journal entries (GJ), adjusting items (AI), and AP entries
# Exclude automated entries, payroll, etc.
transaction_patterns = r'GJ CD|GJ CR|GJ GJ|AI ACCRUE|AI TRSFER|AI TRNSFR|\sAP\s'

tb_filtered = tb[tb['description'].str.contains(transaction_patterns, regex=True, na=False)].copy()

print(f" Step 2: Filtered to {len(tb_filtered):,} manual entries")
print(f" (Excluded {len(tb) - len(tb_filtered):,} automated entries)")
```

---

### Step 3: Extract and Clean Amounts

```python
# Extract amount from description
# Amount could be anywhere after transaction code
tb_filtered['Amount'] = tb_filtered['description'].str.extract(r'([\d,]+\.?\d*-?)')

# Handle trailing dash notation (credit notation)
# "2,500.00-" → "-2,500.00"
mask_credit = tb_filtered['Amount'].str.endswith('-', na=False)
tb_filtered.loc[mask_credit, 'Amount'] = '-' + tb_filtered.loc[mask_credit, 'Amount'].str[:-1]

# Remove commas and convert to float
tb_filtered['Amount'] = tb_filtered['Amount'].str.replace(',', '')
tb_filtered['Amount'] = pd.to_numeric(tb_filtered['Amount'], errors='coerce')

# Remove rows without valid amounts
tb_filtered = tb_filtered[tb_filtered['Amount'].notna()]

print(f" Step 3: Extracted and cleaned amounts")
print(f" Total amount: ${tb_filtered['Amount'].sum():,.2f}")
```

---

### Step 4: Calculate Fiscal Periods

```python
# Convert Month string to datetime
tb_filtered['Month'] = pd.to_datetime(tb_filtered['Month'])

# Calculate fiscal quarter (July-June fiscal year)
tb_filtered['Quarter'] = pd.PeriodIndex(tb_filtered['Month'], freq='Q-JUN').strftime('Q%q')

# Extract month number and calendar year
tb_filtered['Month_number'] = tb_filtered['Month'].dt.month
tb_filtered['Calendar_year'] = tb_filtered['Month'].dt.year

print(f" Step 4: Calculated fiscal periods")
print(f" Quarters: {tb_filtered['Quarter'].unique()}")
```

---

### Step 5: Parse Account Structure

```python
# Extract fund code from account number
# Format: 1234567-[12]-500100
# ^^-- fund code
tb_filtered['Fund_code'] = tb_filtered['Account_num'].str.extract(r'\-(\d{2})\-')
tb_filtered['Fund_code'] = pd.to_numeric(tb_filtered['Fund_code'], errors='coerce')

# Create shortened account number (remove leading zero)
tb_filtered['Account_num_short'] = tb_filtered['Account_num'].str[1:]

print(f" Step 5: Parsed account structure")
print(f" Fund codes found: {tb_filtered['Fund_code'].unique()}")
```

---

### Step 6: Merge with Classification Library

```python
# Load master classification library
library_path = 'Master_Classification_Library.xlsx'
library = pd.read_excel(library_path, sheet_name='special_fund_520', keep_default_na=False)

print(f"\n Loaded classification library:")
print(f" Total mappings: {len(library):,}")

# Use most recent classifications
library_recent = library[library['Year_created'] >= 2023]

# Remove duplicates (keep most recent)
library_clean = library_recent.sort_values(['Account_num', 'Year_created']) \
 .drop_duplicates(subset='Account_num', keep='last')

print(f" Active mappings: {len(library_clean):,}")

# Merge trial balance with classifications
tb_merged = pd.merge(
 tb_filtered,
 library_clean[['Account_num', 'Budget_Category', 'Subcategory', 
 'Report_Line', 'Account_Type', 'Expense_vs_Accrual']],
 on='Account_num',
 how='left',
 indicator=True
)

# Check merge quality
matched = (tb_merged['_merge'] == 'both').sum()
unmatched = (tb_merged['_merge'] == 'left_only').sum()

print(f"\n Step 6: Merged with classifications")
print(f" Matched: {matched:,} rows ({matched/len(tb_merged)*100:.1f}%)")
print(f" Unmatched: {unmatched:,} rows")
```

---

### Step 7: Identify Unmapped Accounts (Data Quality)

```python
# Extract accounts without classifications
unmapped = tb_merged[tb_merged['_merge'] == 'left_only']

if len(unmapped) > 0:
 print(f"\nWarning: {len(unmapped):,} transactions with unmapped accounts")
 
 # Summarize unmapped accounts
 unmapped_summary = unmapped.groupby(['Account_num', 'Account_desc']).agg({
 'Amount': ['count', 'sum']
 }).reset_index()
 
 unmapped_summary.columns = ['Account_num', 'Account_desc', 'Transaction_Count', 'Total_Amount']
 unmapped_summary = unmapped_summary.sort_values('Total_Amount', ascending=False)
 
 # Export for classification
 unmapped_summary.to_excel(
 f'Unmapped_Accounts_{datetime.now():%Y%m%d}.xlsx', 
 index=False
 )
 
 print(f" Exported unmapped accounts for classification")
 print(f"\n Top 5 by dollar amount:")
 print(unmapped_summary.head())
else:
 print(" All accounts are mapped!")
```

---

### Step 8: Filter to Expense Accounts

```python
# Focus on expense accounts (exclude revenue, assets, closing entries)
expense_types = ['E', 'A', 'MA', 'GA', 'M', 'G', 'T', 'TA']
expenses = tb_merged[tb_merged['Account_Type'].isin(expense_types)].copy()

# Exclude closing entries
closing_indicators = ['CL', 'CLOSE', 'CLOSING']
expenses = expenses[~expenses['Account_desc'].str.contains('|'.join(closing_indicators), case=False, na=False)]

print(f"\n Step 8: Filtered to expense accounts")
print(f" Expense transactions: {len(expenses):,}")
print(f" Total expenses: ${expenses['Amount'].sum():,.2f}")
```

---

### Step 9: Create Multi-Dimensional Pivot Analysis

```python
# Create comprehensive pivot table
# Dimensions: Budget Category × Quarter × Month × Expense Type
final_pivot = expenses.pivot_table(
 index=['Budget_Category', 'Subcategory', 'Report_Line'],
 columns=['Quarter', 'Month_number', 'Expense_vs_Accrual'],
 values='Amount',
 aggfunc='sum',
 fill_value=0,
 margins=True # Add totals
)

print(f"\n Step 9: Created multi-dimensional pivot")
print(f" Dimensions: {final_pivot.shape}")
print(f"\nPreview:")
print(final_pivot.head())
```

---

### Step 10: Export Results

```python
# Create Excel workbook with multiple sheets
output_file = f'Expense_Analysis_FY2024_{datetime.now():%Y%m%d}.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
 # Sheet 1: Executive Summary Pivot
 final_pivot.to_excel(writer, sheet_name='Executive Summary')
 
 # Sheet 2: Detail transactions
 expenses[['Month', 'Account_num_short', 'Account_desc', 'Budget_Category', 
 'Subcategory', 'Amount', 'Quarter', 'Expense_vs_Accrual']].to_excel(
 writer, sheet_name='Detail', index=False
 )
 
 # Sheet 3: Monthly Summary
 monthly_summary = expenses.groupby(['Quarter', 'Month_number'])['Amount'].sum().reset_index()
 monthly_summary.to_excel(writer, sheet_name='Monthly Totals', index=False)
 
 # Sheet 4: Budget Category Summary
 category_summary = expenses.groupby('Budget_Category').agg({
 'Amount': 'sum',
 'Account_num': 'nunique'
 }).reset_index()
 category_summary.columns = ['Budget_Category', 'Total_Amount', 'Unique_Accounts']
 category_summary.to_excel(writer, sheet_name='By Category', index=False)

print(f"\n Saved to: {output_file}")
```

---

### Step 11: Generate Summary Statistics

```python
# Print executive summary
print(f"\n" + "="*60)
print(f"FISCAL YEAR 2024 EXPENSE ANALYSIS SUMMARY")
print(f"="*60)

print(f"\n Overall Statistics:")
print(f" Total Transactions: {len(expenses):,}")
print(f" Total Expenses: ${expenses['Amount'].sum():,.2f}")
print(f" Date Range: {expenses['Month'].min():%Y-%m-%d} to {expenses['Month'].max():%Y-%m-%d}")

print(f"\n By Quarter:")
quarterly = expenses.groupby('Quarter')['Amount'].sum()
for quarter, amount in quarterly.items():
 print(f" {quarter}: ${amount:,.2f}")

print(f"\n By Budget Category:")
by_category = expenses.groupby('Budget_Category')['Amount'].sum().sort_values(ascending=False)
for category, amount in by_category.head().items():
 print(f" {category}: ${amount:,.2f}")

print(f"\n Cash vs. Accrual:")
by_type = expenses.groupby('Expense_vs_Accrual')['Amount'].sum()
for exp_type, amount in by_type.items():
 print(f" {exp_type}: ${amount:,.2f}")

print(f"\n Analysis complete! Time: {datetime.now():%H:%M:%S}")
```

---

## Complete Script (Production-Ready)

Here's the entire workflow in one reusable function:

```python
import pandas as pd
import numpy as np
import re
from datetime import datetime

def process_trial_balance(
 input_file,
 library_file,
 output_file=None
):
 """
 Complete trial balance processing workflow
 
 Args:
 input_file: Path to trial balance export
 library_file: Path to classification library
 output_file: Path for output (auto-generated if None)
 
 Returns:
 Dictionary with processed data and metrics
 """
 
 print(f" Starting trial balance processing...")
 print(f" Input: {input_file}")
 print(f" Library: {library_file}\n")
 
 # Step 1: Parse
 tb = pd.read_excel(input_file, header=None, names=['description'])
 tb['description'] = tb['description'].fillna(' ')
 tb[['Account_num', 'Account_desc']] = tb['description'].str.extract(r'(\d{7}\-\d{2}\-\d{6})\s+(.*)')
 tb['Month'] = tb['description'].str.extract(r"([0-9]{2}\/[0-9]{2}\/[0-9]{4})")
 tb['Account_num'] = tb['Account_num'].ffill()
 tb['Account_desc'] = tb['Account_desc'].ffill()
 tb['Month'] = tb['Month'].ffill()
 print(f" Parsed {len(tb):,} rows")
 
 # Step 2: Filter
 tb_filtered = tb[tb['description'].str.contains(
 r'GJ CD|GJ CR|GJ GJ|AI ACCRUE|AI TRSFER|\sAP\s', regex=True, na=False
 )].copy()
 print(f" Filtered to {len(tb_filtered):,} transactions")
 
 # Step 3: Clean amounts
 tb_filtered['Amount'] = tb_filtered['description'].str.extract(r'([\d,]+\.?\d*-?)')
 mask = tb_filtered['Amount'].str.endswith('-', na=False)
 tb_filtered.loc[mask, 'Amount'] = '-' + tb_filtered.loc[mask, 'Amount'].str[:-1]
 tb_filtered['Amount'] = pd.to_numeric(
 tb_filtered['Amount'].str.replace(',', ''), errors='coerce'
 )
 tb_filtered = tb_filtered[tb_filtered['Amount'].notna()]
 print(f" Cleaned amounts: ${tb_filtered['Amount'].sum():,.2f}")
 
 # Step 4: Fiscal periods
 tb_filtered['Month'] = pd.to_datetime(tb_filtered['Month'])
 tb_filtered['Quarter'] = pd.PeriodIndex(tb_filtered['Month'], freq='Q-JUN').strftime('Q%q')
 tb_filtered['Month_number'] = tb_filtered['Month'].dt.month
 print(f" Calculated fiscal quarters")
 
 # Step 5: Parse account structure
 tb_filtered['Fund_code'] = tb_filtered['Account_num'].str.extract(r'\-(\d{2})\-')
 tb_filtered['Account_num_short'] = tb_filtered['Account_num'].str[1:]
 
 # Step 6: Merge with library
 library = pd.read_excel(library_file, keep_default_na=False)
 library_clean = library.sort_values(['Account_num', 'Year_created']) \
 .drop_duplicates(subset='Account_num', keep='last')
 
 tb_merged = pd.merge(
 tb_filtered,
 library_clean[['Account_num', 'Budget_Category', 'Account_Type', 'Expense_vs_Accrual']],
 on='Account_num',
 how='left',
 indicator=True
 )
 print(f" Merged with classifications")
 
 # Step 7: Handle unmapped
 unmapped = tb_merged[tb_merged['_merge'] == 'left_only']
 if len(unmapped) > 0:
 unmapped_file = f'Unmapped_Accounts_{datetime.now():%Y%m%d_%H%M%S}.xlsx'
 unmapped.groupby(['Account_num', 'Account_desc'])['Amount'].sum() \
 .reset_index().to_excel(unmapped_file, index=False)
 print(f"Warning: {len(unmapped)} unmapped → {unmapped_file}")
 
 # Step 8: Filter expenses
 expenses = tb_merged[tb_merged['Account_Type'].isin(['E', 'A', 'MA', 'GA'])].copy()
 print(f" Filtered to {len(expenses):,} expense transactions")
 
 # Step 9: Create pivot
 final_pivot = expenses.pivot_table(
 index='Budget_Category',
 columns=['Quarter', 'Expense_vs_Accrual'],
 values='Amount',
 aggfunc='sum',
 fill_value=0,
 margins=True
 )
 
 # Step 10: Export
 if output_file is None:
 output_file = f'Expense_Analysis_{datetime.now():%Y%m%d_%H%M%S}.xlsx'
 
 with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
 final_pivot.to_excel(writer, sheet_name='Summary')
 expenses.to_excel(writer, sheet_name='Detail', index=False)
 
 print(f"\n Saved to: {output_file}")
 print(f" Processing complete!\n")
 
 # Return metrics
 return {
 'total_transactions': len(expenses),
 'total_amount': expenses['Amount'].sum(),
 'unmapped_count': len(unmapped),
 'output_file': output_file,
 'data': expenses,
 'pivot': final_pivot
 }

# Usage:
results = process_trial_balance(
 'trial_balance_fy2024.xlsx',
 'Master_Classification_Library.xlsx'
)

print(f"Total Expenses: ${results['total_amount']:,.2f}")
```

---

## What We Accomplished

### Input → Output:

**Started with:**
- Messy text report with 2,500 lines
- Unstructured data
- Multiple formats
- Some unmapped accounts

**Ended with:**
- Clean multi-dimensional analysis
- Executive summary pivot
- Detail transaction list
- Monthly/quarterly summaries
- List of accounts needing classification

### Time Comparison:

| Step | Manual (Excel) | Python |
|------|----------------|--------|
| Import & parse | 20 min | 5 sec |
| Clean amounts | 15 min | 2 sec |
| Calculate quarters | 20 min | 1 sec |
| Merge classifications | 25 min | 3 sec |
| Create pivots | 45 min | 2 sec |
| Format & export | 30 min | 5 sec |
| **TOTAL** | **~2.5 hours** | **< 30 sec** |

**Time saved:** 99.7% 

---

## Patterns Combined in This Workflow

 **Pattern 1:** Legacy text parsing (str.extract + ffill) 
 **Pattern 2:** Credit/debit notation conversion 
 **Pattern 3:** Custom classification functions 
 **Pattern 4:** Multi-level pivot tables 
 **Pattern 5:** Fiscal year/quarter calculations 
 **Pattern 6:** String cleaning & normalization 
 **Pattern 8:** Master mapping integration 
 **Pattern 13:** Duplicate detection

**All in one workflow!**

---

## Try It Yourself!

### Download Sample Files:

1. **Sample trial balance:** [link]
2. **Classification library template:** [link]
3. **Complete script:** [link]

### Run in 3 Steps:

```python
# 1. Install pandas
pip install pandas openpyxl

# 2. Update file paths
input_file = 'your_trial_balance.xlsx'
library_file = 'your_classifications.xlsx'

# 3. Run!
results = process_trial_balance(input_file, library_file)
```

---

## Benefits

 **Speed:** 2.5 hours → 30 seconds (99.7% faster) 
 **Consistency:** Same process every month 
 **Quality:** Automatic error detection 
 **Auditability:** Complete processing trail 
 **Scalability:** Handle 10× more data easily 
 **Professional:** Executive-ready output

---

## What's Next?

### Customize This Workflow:

- Adapt regex patterns for your account format
- Modify fiscal year-end (change `Q-JUN` to your fiscal end)
- Adjust transaction filters
- Customize classification logic
- Add your own summary metrics

### Level Up:

- **Automate monthly:** Schedule with Task Scheduler/cron
- **Email reports:** Use smtplib to auto-send
- **Add visualizations:** Create charts with matplotlib
- **Database integration:** Pull data directly from SQL

---

## Your Turn!

**Want to adapt this for your organization?** Share your trial balance format in the comments!

**Already automated your workflow?** Share your time savings story!

**Stuck on a step?** Ask for help - we're here!

---

**Tags:** #Python #Pandas #Workflow #Automation #TrialBalance #EndToEnd #FinanceAutomation

---

*The ultimate post combining ALL techniques. From chaos to clarity in minutes!*
