---
layout: primer_post
title: "🗺️ Master Data Mapping: End Classification Chaos"
subtitle: "Your team classifies the same account three different ways across different reports. Here's how to establish data governance that actually works."
tags: [python, pandas, data-governance, master-data, classifications, accounting, data-quality]
comments: true
author: PANDAUDIT Team
---

## The Classification Nightmare

**Month 1:** Account 1234567 is classified as "Personnel Expenses"  
**Month 2:** Same account shows up as "Salary & Benefits"  
**Month 3:** Now it's "Administrative Costs"

**Result?** Your year-over-year analysis is useless. Auditors are confused. Management doesn't trust your numbers.

Sound familiar? You need a **master mapping library** - and Python makes it bulletproof.

---

## The Problem: Classification Inconsistencies

### What Goes Wrong:

1. **Multiple people classifying** → Different interpretations
2. **No central source of truth** → Everyone has their own Excel file
3. **Changes not tracked** → Can't audit classification history
4. **No validation** → Errors caught months later (or never)

### The Excel Approach (Broken):

```
Classification_2023.xlsx  (on Mary's desktop)
Classification_2024_v2.xlsx  (on John's desktop)
Classification_FINAL.xlsx  (on the shared drive)
Classification_FINAL_FINAL.xlsx  (also on the shared drive 🤦)
```

**Problems:**
- Which version is correct?
- Who changed what and when?
- How do we detect inconsistencies?
- Can't automate with confidence

---

## The Solution: Python-Powered Master Mapping

### Architecture:

```
┌─────────────────────────────────────┐
│   Master Classification Library     │
│   (Single source of truth Excel)    │
└──────────────┬──────────────────────┘
               │
               │ Python reads & validates
               │
       ┌───────▼────────┐
       │  Quality Checks │
       │  - Duplicates   │
       │  - Inconsist.   │
       │  - Missing      │
       └───────┬─────────┘
               │
               │ Merge with transactions
               │
       ┌───────▼──────────┐
       │  Classified Data  │
       │  (Ready for       │
       │   reporting)      │
       └──────────────────┘
```

---

## Step 1: Create the Master Mapping Library

### Excel Structure:

| Account_num | Account_desc | Category | Subcategory | Report_Line | Year_created |
|-------------|--------------|----------|-------------|-------------|--------------|
| 1234567-01-000100 | Salaries & Wages | Personnel | Salaries | Line 10 | 2024 |
| 1234567-01-000200 | Health Insurance | Personnel | Benefits | Line 11 | 2024 |
| 2345678-02-000300 | Office Supplies | Operations | Supplies | Line 20 | 2023 |

**Key fields:**
- `Account_num` = Unique identifier
- `Category` / `Subcategory` = Multi-level classification
- `Report_Line` = Where it appears on financial statements
- `Year_created` = Track when classification was added

---

## Step 2: Load and Validate the Library

```python
import pandas as pd

# Load master classification library
library_path = '/path/to/Master_Classifications.xlsx'
library = pd.read_excel(library_path, sheet_name='Mappings', keep_default_na=False)

print(f"📚 Loaded {len(library):,} classifications from master library")

# Basic info
print(f"   Unique accounts: {library['Account_num'].nunique()}")
print(f"   Categories: {library['Category'].nunique()}")
print(f"   Date range: {library['Year_created'].min()} - {library['Year_created'].max()}")
```

---

## Step 3: Detect Classification Inconsistencies

### Problem: Same Account, Different Classifications

```python
# Find accounts with multiple classifications across years
inconsistent_accounts = library.groupby('Account_num')['Category'].nunique()
problems = inconsistent_accounts[inconsistent_accounts > 1]

if len(problems) > 0:
    print(f"⚠️  WARNING: {len(problems)} accounts have multiple classifications!")
    
    # Generate detailed report for review
    problem_details = library[library['Account_num'].isin(problems.index)]
    problem_details = problem_details.sort_values(['Account_num', 'Year_created'])
    
    # Show examples
    print("\nExamples of inconsistent classifications:")
    print(problem_details[['Account_num', 'Account_desc', 'Category', 'Year_created']].head(10))
    
    # Export full report for team review
    problem_details.to_excel('REVIEW_NEEDED_Classifications.xlsx', index=False)
    print(f"\n📋 Full report saved to: REVIEW_NEEDED_Classifications.xlsx")
else:
    print("✅ All classifications are consistent!")
```

### What This Catches:

- Account reclassifications that weren't intentional
- Typos in category names (`"Personnel"` vs `"Personel"`)
- Different people using different category names for same concept

---

## Step 4: Deduplicate and Keep Most Recent

### Strategy: Trust the Latest Classification

```python
# Sort by year (most recent first)
library_sorted = library.sort_values(by=['Account_num', 'Year_created'], ascending=[True, False])

# Keep only most recent classification per account
library_clean = library_sorted.drop_duplicates(
    subset=['Account_num'], 
    keep='first'  # Keep first row (most recent due to sort)
)

print(f"✂️  Deduplicated: {len(library)} → {len(library_clean)} classifications")
print(f"   Removed {len(library) - len(library_clean)} outdated mappings")
```

**Alternative:** Keep all history but add `is_active` flag:

```python
# Mark only most recent as active
library['is_active'] = False
library.loc[library.groupby('Account_num')['Year_created'].idxmax(), 'is_active'] = True

# Use only active classifications
library_active = library[library['is_active'] == True]
```

---

## Step 5: Merge with Transaction Data

### The Main Event: Classify Your Transactions

```python
# Load transaction data (e.g., trial balance)
transactions = pd.read_excel('trial_balance_december.xlsx')

print(f"💰 Loaded {len(transactions):,} transactions")

# Merge with master classifications
df_classified = pd.merge(
    transactions,
    library_clean[['Account_num', 'Category', 'Subcategory', 'Report_Line']],
    on='Account_num',
    how='left',
    indicator=True  # Track which records matched
)

# Check merge quality
merge_stats = df_classified['_merge'].value_counts()
print("\n📊 Merge Results:")
print(f"   ✅ Matched (both): {merge_stats.get('both', 0):,}")
print(f"   ⚠️  Unmatched transactions: {merge_stats.get('left_only', 0):,}")
print(f"   ℹ️  Unused mappings: {merge_stats.get('right_only', 0):,}")
```

---

## Step 6: Handle Unmapped Accounts

### New Accounts Need Classification!

```python
# Extract unmapped accounts
unmapped = df_classified[df_classified['_merge'] == 'left_only']

if len(unmapped) > 0:
    print(f"\n⚠️  {len(unmapped):,} transactions with unmapped accounts!")
    
    # Get unique unmapped accounts
    new_accounts = unmapped[['Account_num', 'Account_desc']].drop_duplicates()
    
    # Calculate total amount for each (prioritize high-dollar accounts)
    new_accounts_summary = unmapped.groupby(['Account_num', 'Account_desc'])['Amount'].agg([
        'count',
        'sum'
    ]).reset_index()
    new_accounts_summary.columns = ['Account_num', 'Account_desc', 'Transaction_count', 'Total_amount']
    
    # Sort by total amount (prioritize large $ accounts)
    new_accounts_summary = new_accounts_summary.sort_values('Total_amount', ascending=False)
    
    # Export for team to classify
    new_accounts_summary.to_excel('NEW_ACCOUNTS_TO_CLASSIFY.xlsx', index=False)
    
    print(f"📋 List of new accounts exported for classification")
    print(f"\nTop 5 by dollar amount:")
    print(new_accounts_summary.head())
else:
    print("✅ All accounts are mapped!")
```

---

## Step 7: Complete Classification Workflow

### Production-Ready Script

```python
import pandas as pd
from datetime import datetime

def classify_transactions(transaction_file, library_file):
    """
    Classify transactions using master mapping library
    
    Returns:
        - Classified DataFrame
        - Quality metrics dictionary
    """
    
    # Load data
    print(f"📂 Loading data...")
    transactions = pd.read_excel(transaction_file)
    library = pd.read_excel(library_file, sheet_name='Mappings', keep_default_na=False)
    
    # Validate library for inconsistencies
    print(f"🔍 Validating master library...")
    inconsistent = library.groupby('Account_num')['Category'].nunique()
    inconsistent_accounts = inconsistent[inconsistent > 1]
    
    if len(inconsistent_accounts) > 0:
        print(f"   ⚠️  {len(inconsistent_accounts)} accounts have inconsistent classifications")
        problem_report = library[library['Account_num'].isin(inconsistent_accounts.index)]
        problem_report.to_excel(f'Inconsistent_Classifications_{datetime.now():%Y%m%d}.xlsx', index=False)
    
    # Deduplicate (keep most recent)
    library_clean = library.sort_values(['Account_num', 'Year_created']) \
                          .drop_duplicates(subset='Account_num', keep='last')
    
    # Merge
    print(f"🔗 Merging transactions with classifications...")
    classified = pd.merge(
        transactions,
        library_clean[['Account_num', 'Category', 'Subcategory', 'Report_Line']],
        on='Account_num',
        how='left',
        indicator=True
    )
    
    # Calculate metrics
    total_txns = len(classified)
    mapped_txns = (classified['_merge'] == 'both').sum()
    unmapped_txns = (classified['_merge'] == 'left_only').sum()
    
    metrics = {
        'total_transactions': total_txns,
        'mapped': mapped_txns,
        'unmapped': unmapped_txns,
        'coverage_pct': (mapped_txns / total_txns * 100) if total_txns > 0 else 0
    }
    
    # Export unmapped accounts if any
    if unmapped_txns > 0:
        unmapped = classified[classified['_merge'] == 'left_only']
        unmapped_summary = unmapped.groupby(['Account_num', 'Account_desc'])['Amount'] \
                                   .agg(['count', 'sum']) \
                                   .reset_index() \
                                   .sort_values('sum', ascending=False)
        unmapped_summary.to_excel(f'Unmapped_Accounts_{datetime.now():%Y%m%d}.xlsx', index=False)
        print(f"   📋 Exported {len(unmapped_summary)} unmapped accounts for classification")
    
    # Print summary
    print(f"\n✅ Classification complete!")
    print(f"   Total transactions: {metrics['total_transactions']:,}")
    print(f"   Mapped: {metrics['mapped']:,} ({metrics['coverage_pct']:.1f}%)")
    print(f"   Unmapped: {metrics['unmapped']:,}")
    
    return classified, metrics

# Usage:
classified_data, quality_metrics = classify_transactions(
    'trial_balance.xlsx',
    'Master_Classifications.xlsx'
)

# Export classified data
classified_data.to_excel('trial_balance_CLASSIFIED.xlsx', index=False)
```

---

## Bonus: Classification Coverage Dashboard

```python
def generate_classification_report(classified_df):
    """Generate summary report of classification coverage"""
    
    report = {
        'By Category': classified_df.groupby('Category')['Amount'].sum().sort_values(ascending=False),
        'By Subcategory': classified_df.groupby(['Category', 'Subcategory'])['Amount'].sum(),
        'Unmapped Amount': classified_df[classified_df['Category'].isnull()]['Amount'].sum()
    }
    
    # Write to Excel with multiple sheets
    with pd.ExcelWriter('Classification_Report.xlsx') as writer:
        for sheet_name, data in report.items():
            if isinstance(data, pd.Series):
                data.to_frame().to_excel(writer, sheet_name=sheet_name)
    
    print("📊 Classification report generated!")

# Generate report
generate_classification_report(classified_data)
```

---

## Benefits of This Approach

✅ **Data Governance:**
- Single source of truth for all classifications
- Audit trail (Year_created field tracks changes)
- Inconsistencies detected automatically

✅ **Quality Control:**
- Unmapped accounts identified immediately
- Classification coverage metrics tracked
- Prioritization by dollar amount

✅ **Efficiency:**
- Classify once, use everywhere
- Automated merge eliminates manual VLOOKUP
- Reusable script for monthly processing

✅ **Collaboration:**
- Export reports for team review
- Clear process for adding new classifications
- Version control friendly (can track library changes in Git)

---

## Time Savings

| Task | Manual (Excel) | Python Automated |
|------|----------------|------------------|
| Monthly classification | 2-3 hours | 2 minutes |
| Find inconsistencies | "Never happens" | Automatic detection |
| Track classification changes | Impossible | Audit trail built-in |
| Generate coverage reports | 30 minutes | 5 seconds |

---

## Try It Yourself!

### Step 1: Create a simple master library

```python
import pandas as pd

# Create sample master library
library = pd.DataFrame({
    'Account_num': ['1234567', '1234568', '2345678'],
    'Account_desc': ['Salaries', 'Benefits', 'Supplies'],
    'Category': ['Personnel', 'Personnel', 'Operations'],
    'Subcategory': ['Salaries', 'Benefits', 'Office'],
    'Report_Line': ['Line 10', 'Line 11', 'Line 20'],
    'Year_created': [2024, 2024, 2023]
})

library.to_excel('Master_Classifications.xlsx', index=False)
print("✅ Master library created!")
```

### Step 2: Classify some transactions

```python
# Sample transaction data
transactions = pd.DataFrame({
    'Date': ['2024-12-15', '2024-12-16', '2024-12-17'],
    'Account_num': ['1234567', '1234568', '9999999'],  # Note: 9999999 not in library!
    'Amount': [50000, 10000, 500]
})

# Merge with classifications
classified = pd.merge(
    transactions,
    library[['Account_num', 'Category', 'Subcategory']],
    on='Account_num',
    how='left',
    indicator=True
)

print("\nClassified transactions:")
print(classified)

# Find unmapped
unmapped = classified[classified['_merge'] == 'left_only']
if len(unmapped) > 0:
    print(f"\n⚠️  {len(unmapped)} unmapped transactions found!")
```

---

## What's Next?

Now that you have master data governance:
- **Multi-year consolidation** → [Read this post](/2026-01-18-multi-year-data-consolidation)
- **Advanced pivot reporting** → [Read this post](/2026-01-12-pivot-tables-on-steroids-multi-level-analysis-in-one-line)
- **End-to-end workflow** → [Read this post](/2026-01-20-end-to-end-workflow-example)

---

## Your Turn!

**How do you currently manage classifications?** Share your challenges in the comments!

**Want to see this adapted for your industry?** Let us know!

---

**Tags:** #Python #Pandas #DataGovernance #MasterData #Classifications #DataQuality #Accounting

---

*Part of the "Data Integration & Quality" series. Master your data, master your reports!*
