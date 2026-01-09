---
layout: primer_post
title: "🚀 The Great Spreadsheet Migration: Moving 20 Years of Data"
subtitle: "How we escaped Excel hell and lived to tell the tale"
tags: [python, pandas, migration, data-consolidation, automation, success-story]
comments: true
author: PANDAUDIT Team
---

## The Announcement That Changed Everything

**CFO (in all-hands meeting):** "We're implementing a new financial system. All historical data must be migrated by year-end."

**Me:** *raises hand* "How much historical data?"

**CFO:** "20 years."

**Me:** "And it's currently in...?"

**CFO:** "Excel. About 2,400 different files."

**Everyone:** *collective groan* 😱

**CFO:** "Budget for migration: $50,000 for consultants."

**Me (internal monologue):** *Or... I could learn Python and do it myself...* 🤔

---

## The Challenge

### The Source Data (AKA: The Nightmare)

**2,400 Excel files containing:**
- Trial balances (monthly, 1995-2024)
- Investment transactions (daily, 2000-2024)
- Member contributions (monthly, 1995-2024)
- Benefit payments (monthly, 1995-2024)
- Employer remittances (monthly, 1995-2024)

**File Formats:**
- 📦 `.xls` (Excel 97-2003) → 1,200 files
- 📄 `.xlsx` (Excel 2007+) → 1,000 files
- 📃 `.xlsb` (Binary) → 150 files
- 📝 `.csv` (supposedly) → 50 files (actually pipe-delimited 🙄)

**File Naming Conventions:**
- `Trial Balance 01-2024.xlsx`
- `TB_January_2024_FINAL.xlsx`
- `TB_Jan2024_v3_REALLY_FINAL.xlsx`
- `Trial_Bal_2024_01_USE_THIS_ONE.xlsx`
- `TB 202401.xls`
- `trial balance january 2024 (2).xlsx`

**Translation:** No consistent naming. Complete chaos. 🔥

**Data Structure:**
- Different column names across years
- Different sheet names
- Some months missing
- Some duplicates (which version is correct? *¯\\_(ツ)_/¯*)
- Formulas instead of values
- Hidden sheets with "backup data"
- Merged cells 🤦
- Colors indicating... something (documentation lost)

---

## The Manual Approach (Estimated)

**Consultants' Proposal:**

1. **Inventory all files** → 2 weeks
2. **Standardize format** → 8 weeks
3. **Consolidate by year** → 12 weeks
4. **Data quality checks** → 4 weeks
5. **Export to new system format** → 2 weeks
6. **Validation** → 4 weeks

**Total Time:** 32 weeks (8 months!)

**Total Cost:** $50,000

**Risk:** High (manual = errors)

---

## The Python Approach

**My Pitch to CFO:**

"Give me 2 weeks to build an automated solution. If it works, we save $50,000 and 7 months. If it doesn't, we hire the consultants."

**CFO:** "You have 1 week."

**Me:** *gulp* 😅

---

## Day 1: File Inventory & Pattern Detection

### Step 1: Find All Excel Files

```python
import os
import pandas as pd
from pathlib import Path

# Find all Excel files recursively
base_path = Path('/data/historical')
excel_files = []

for ext in ['*.xls', '*.xlsx', '*.xlsb']:
    excel_files.extend(base_path.rglob(ext))

print(f"Found {len(excel_files)} Excel files")

# Create inventory
inventory = pd.DataFrame({
    'File_Path': [str(f) for f in excel_files],
    'File_Name': [f.name for f in excel_files],
    'File_Size_MB': [f.stat().st_size / 1024 / 1024 for f in excel_files],
    'Modified_Date': [pd.Timestamp.fromtimestamp(f.stat().st_mtime) for f in excel_files]
})

# Detect file type from name
inventory['File_Type'] = inventory['File_Name'].apply(lambda x: 
    'Trial_Balance' if 'TB' in x.upper() or 'TRIAL' in x.upper() else
    'Investments' if 'INV' in x.upper() else
    'Contributions' if 'CONTRIB' in x.upper() else
    'Benefits' if 'BEN' in x.upper() else
    'Unknown'
)

inventory.to_excel('file_inventory.xlsx', index=False)

print(inventory['File_Type'].value_counts())
```

**Output:**
```
Found 2,413 Excel files

File_Type
Trial_Balance    1,247
Investments        687
Contributions      289
Benefits           156
Unknown             34
```

**Time:** 5 minutes ⚡

---

### Step 2: Detect Sheet Names

```python
import openpyxl

# Sample 100 files to detect sheet name patterns
sample_files = inventory.sample(100)

sheet_names = []
for file_path in sample_files['File_Path']:
    try:
        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        sheet_names.extend(wb.sheetnames)
        wb.close()
    except:
        pass

# Count most common sheet names
from collections import Counter
sheet_counts = Counter(sheet_names)

print("Most common sheet names:")
for name, count in sheet_counts.most_common(20):
    print(f"  {name}: {count}")
```

**Output:**
```
Most common sheet names:
  Sheet1: 234
  Data: 187
  Trial Balance: 156
  TB: 98
  2024: 67
  Summary: 45
  Detail: 34
  ...
```

**Insight:** Try "Data" first, then "Trial Balance", then first sheet.

---

## Day 2: Build Robust File Reader

### The Universal Excel Reader

```python
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def read_excel_robust(file_path):
    """
    Reads an Excel file, trying multiple strategies
    Returns: DataFrame or None
    """
    # Strategy 1: Try common sheet names
    common_sheets = ['Data', 'Trial Balance', 'TB', 'Detail', 'Sheet1']
    
    for sheet in common_sheets:
        try:
            df = pd.read_excel(file_path, sheet_name=sheet)
            if len(df) > 0:  # Not empty
                return df, sheet
        except:
            pass
    
    # Strategy 2: Try first sheet
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        if len(df) > 0:
            return df, 'First_Sheet'
    except:
        pass
    
    # Strategy 3: Try reading as CSV (for .csv mislabeled as .xls)
    try:
        df = pd.read_csv(file_path, encoding='latin-1')
        if len(df) > 0:
            return df, 'CSV'
    except:
        pass
    
    return None, None

# Test on sample
results = []
for file_path in inventory['File_Path'].head(100):
    df, sheet = read_excel_robust(file_path)
    results.append({
        'File': file_path,
        'Success': df is not None,
        'Sheet': sheet,
        'Rows': len(df) if df is not None else 0,
        'Columns': len(df.columns) if df is not None else 0
    })

results_df = pd.DataFrame(results)
print(f"Success rate: {results_df['Success'].mean()*100:.1f}%")
```

**Output:**
```
Success rate: 94.2%
```

**Not bad! Fix the 5.8% failures manually.** ✅

---

## Day 3: Column Name Standardization

### The Problem

**1995 files:** `Acct_Num`, `Description`, `Debit`, `Credit`  
**2005 files:** `Account Number`, `Account Description`, `Debit Amount`, `Credit Amount`  
**2015 files:** `Account`, `Desc`, `DR`, `CR`  
**2024 files:** `GL_Account`, `GL_Description`, `Debit_Amt`, `Credit_Amt`

**Goal:** Map all variations to standard column names

---

### The Solution: Fuzzy Matching

```python
from fuzzywuzzy import fuzz

# Standard column names
standard_columns = {
    'Account_Number': ['account', 'acct', 'gl_account', 'account_num', 'account number'],
    'Description': ['desc', 'description', 'account_desc', 'account description', 'name'],
    'Debit': ['debit', 'dr', 'debit_amt', 'debit amount', 'debit_amount'],
    'Credit': ['credit', 'cr', 'credit_amt', 'credit amount', 'credit_amount'],
    'Date': ['date', 'transaction_date', 'trans_date', 'posting_date'],
    'Amount': ['amount', 'amt', 'balance', 'value']
}

def standardize_columns(df):
    """Map column names to standard names using fuzzy matching"""
    column_mapping = {}
    
    for col in df.columns:
        col_lower = str(col).lower().strip()
        
        # Try exact match first
        for standard, variations in standard_columns.items():
            if col_lower in variations:
                column_mapping[col] = standard
                break
        
        # Try fuzzy match (80% threshold)
        if col not in column_mapping:
            best_match = None
            best_score = 0
            
            for standard, variations in standard_columns.items():
                for variation in variations:
                    score = fuzz.ratio(col_lower, variation)
                    if score > best_score and score > 80:
                        best_score = score
                        best_match = standard
            
            if best_match:
                column_mapping[col] = best_match
    
    return df.rename(columns=column_mapping)

# Test
test_df = pd.DataFrame(columns=['Acct_Num', 'Desc', 'DR', 'CR'])
standardized = standardize_columns(test_df)
print(standardized.columns.tolist())
# Output: ['Account_Number', 'Description', 'Debit', 'Credit']
```

**Success!** 🎉

---

## Day 4: Data Extraction & Consolidation

```python
import pandas as pd
from tqdm import tqdm  # Progress bar

def process_all_files(file_type='Trial_Balance'):
    """Process all files of a given type"""
    # Filter inventory
    files = inventory[inventory['File_Type'] == file_type].copy()
    
    print(f"Processing {len(files)} {file_type} files...")
    
    all_data = []
    failed_files = []
    
    for idx, row in tqdm(files.iterrows(), total=len(files)):
        try:
            # Read file
            df, sheet = read_excel_robust(row['File_Path'])
            
            if df is None:
                failed_files.append(row['File_Name'])
                continue
            
            # Standardize columns
            df = standardize_columns(df)
            
            # Add metadata
            df['Source_File'] = row['File_Name']
            df['Source_Sheet'] = sheet
            df['File_Modified_Date'] = row['Modified_Date']
            
            # Extract date from filename (if possible)
            # Pattern: "TB_01_2024" or "Trial Balance January 2024"
            import re
            date_match = re.search(r'(\d{1,2})[_\s-]?(\d{4})', row['File_Name'])
            if date_match:
                month, year = date_match.groups()
                df['Report_Month'] = int(month)
                df['Report_Year'] = int(year)
            
            all_data.append(df)
            
        except Exception as e:
            failed_files.append(f"{row['File_Name']}: {str(e)}")
    
    # Consolidate
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        print(f"\nConsolidated {len(combined):,} rows from {len(all_data)} files")
        print(f"Failed: {len(failed_files)} files")
        
        # Export
        combined.to_parquet(f'{file_type}_consolidated.parquet')  # Faster than Excel!
        
        if failed_files:
            pd.DataFrame({'Failed_Files': failed_files}).to_excel(
                f'{file_type}_failed.xlsx', index=False
            )
        
        return combined
    else:
        print("No data extracted!")
        return None

# Process all trial balances
tb_data = process_all_files('Trial_Balance')
```

**Output:**
```
Processing 1,247 Trial_Balance files...
100%|██████████| 1247/1247 [12:34<00:00, 1.65it/s]

Consolidated 2,847,392 rows from 1,198 files
Failed: 49 files
```

**Time:** 12 minutes (for 1,247 files!) ⚡

**Manually review 49 failed files (corrupt, password-protected, etc.)**

---

## Day 5: Data Quality Checks

### Check #1: Completeness (Missing Months)

```python
# Check for missing months
expected_months = pd.date_range(start='1995-01', end='2024-12', freq='MS')
actual_months = tb_data.groupby(['Report_Year', 'Report_Month']).size().reset_index()
actual_months['Period'] = pd.to_datetime(
    actual_months['Report_Year'].astype(str) + '-' + 
    actual_months['Report_Month'].astype(str).str.zfill(2) + '-01'
)

missing_months = set(expected_months) - set(actual_months['Period'])

print(f"Missing months: {len(missing_months)}")
if missing_months:
    print(sorted(missing_months))
```

---

### Check #2: Duplicates

```python
# Check for duplicate months (multiple versions)
duplicates = actual_months[actual_months.duplicated(subset=['Report_Year', 'Report_Month'], keep=False)]

if len(duplicates) > 0:
    print(f"Duplicate months found: {len(duplicates)}")
    print(duplicates[['Report_Year', 'Report_Month', 'Source_File']].head(20))
    
    # Keep most recent file (by modified date)
    tb_data = tb_data.sort_values('File_Modified_Date').drop_duplicates(
        subset=['Report_Year', 'Report_Month', 'Account_Number'],
        keep='last'
    )
```

---

### Check #3: Trial Balance Validation

```python
# Verify debits = credits for each month
validation = tb_data.groupby(['Report_Year', 'Report_Month']).agg({
    'Debit': 'sum',
    'Credit': 'sum'
}).reset_index()

validation['Difference'] = validation['Debit'] - validation['Credit']
validation['Balances'] = abs(validation['Difference']) < 0.01  # Allow $0.01 rounding

print(f"Months in balance: {validation['Balances'].sum()} / {len(validation)}")

if not validation['Balances'].all():
    print("\nMonths out of balance:")
    print(validation[~validation['Balances']])
```

**Output:**
```
Months in balance: 358 / 360

Months out of balance:
   Report_Year  Report_Month      Debit     Credit  Difference
45        1998             6  1,234,567  1,234,569       -2.00
67        2001             2  2,456,789  2,456,790       -1.00
```

**Action:** Investigate 2 months manually (likely data entry errors in source)

---

## Day 6: Export to New System Format

### Target System Requirements

**Format:** CSV, pipe-delimited (`|`), specific column order, date format `YYYYMMDD`

```python
# Transform to target format
tb_export = tb_data[[
    'Report_Year',
    'Report_Month',
    'Account_Number',
    'Description',
    'Debit',
    'Credit'
]].copy()

# Create period field (YYYYMM)
tb_export['Period'] = (
    tb_export['Report_Year'].astype(str) + 
    tb_export['Report_Month'].astype(str).str.zfill(2)
)

# Format amounts (2 decimal places, no commas)
tb_export['Debit'] = tb_export['Debit'].round(2)
tb_export['Credit'] = tb_export['Credit'].round(2)

# Reorder columns
tb_export = tb_export[[
    'Period',
    'Account_Number',
    'Description',
    'Debit',
    'Credit'
]]

# Export as pipe-delimited CSV
tb_export.to_csv(
    'trial_balance_MIGRATION.csv',
    sep='|',
    index=False,
    header=True
)

print(f"Exported {len(tb_export):,} rows to trial_balance_MIGRATION.csv")
print(f"File size: {os.path.getsize('trial_balance_MIGRATION.csv') / 1024 / 1024:.1f} MB")
```

**Output:**
```
Exported 2,847,392 rows to trial_balance_MIGRATION.csv
File size: 187.3 MB
```

---

## Day 7: The Presentation

**Me (to CFO and finance team):**

"I've consolidated 20 years of trial balances. 2.8 million rows from 1,247 Excel files."

**CFO:** "That's... impressive. How long did it take?"

**Me:** "About 6 days. Most of that was building the automation. Once it's running, it processes all files in 12 minutes."

**Finance Director:** "The consultants quoted 8 months..."

**Me:** "I know. Here's the validation report. 358 of 360 months balance perfectly. These 2 need manual review—they were already wrong in the source files."

**CFO:** *scrolls through validation report* "This is incredibly detailed. Can you do the same for investments, contributions, and benefits?"

**Me:** "Already done. Ran the same scripts on all file types. Total: 7.2 million rows consolidated."

**CFO:** "How much did this cost?"

**Me:** "Zero. Well, I bought a Python course for $50."

**CFO:** *long pause* "You saved us $50,000 and 7 months. I'm giving you a bonus. And a promotion. And I want you to train the whole team."

**Me:** *tries not to cry* 🥹

---

## The Results

### Before Python:
- ⏰ **Estimated Time:** 8 months
- 💰 **Estimated Cost:** $50,000
- 🐛 **Risk:** High (manual = errors)
- 😓 **Stress:** Off the charts

### After Python:
- ⏰ **Actual Time:** 1 week
- 💰 **Actual Cost:** $50 (online course)
- ✅ **Accuracy:** 99.4% automated (6 files needed manual fix)
- 😊 **Stress:** Manageable

### Metrics:
- **Files Processed:** 2,413
- **Rows Consolidated:** 7,241,039
- **Time Saved:** 32 weeks
- **Money Saved:** $50,000
- **ROI:** 100,000% 💥

---

## The Scripts I Built

### 1. File Inventory Script
```python
inventory_files.py
```
- Recursively finds all Excel files
- Detects file type from name
- Creates inventory spreadsheet

### 2. Universal Excel Reader
```python
read_excel_robust.py
```
- Tries multiple strategies to read files
- Handles .xls, .xlsx, .xlsb, .csv
- Returns DataFrame or None

### 3. Column Standardizer
```python
standardize_columns.py
```
- Maps column name variations to standard names
- Uses fuzzy matching
- Handles typos and abbreviations

### 4. Consolidation Script
```python
consolidate_files.py
```
- Processes all files of a given type
- Extracts dates from filenames
- Adds metadata (source file, sheet, modified date)
- Exports to Parquet (faster than Excel)

### 5. Validation Script
```python
validate_data.py
```
- Checks for missing months
- Identifies duplicates
- Validates trial balance (debits = credits)
- Generates quality report

### 6. Export Script
```python
export_to_new_system.py
```
- Transforms to target system format
- Handles special formatting requirements
- Exports as pipe-delimited CSV

**Total Lines of Code:** ~800 (including comments)

**Reusable:** Yes! Used for 4 different data types with minor tweaks.

---

## Lessons Learned

### Lesson #1: Automation Beats Manual Every Time

**Manual Approach:**
- Time: 8 months
- Cost: $50,000
- Errors: Unknown (probably many)

**Automated Approach:**
- Time: 1 week
- Cost: $50
- Errors: 6 files out of 2,413 (0.25%)

**Winner:** Automation 🏆

---

### Lesson #2: Invest in Robust Error Handling

Files WILL be:
- Corrupt
- Password-protected
- In unexpected formats
- Mislabeled
- Empty

**Handle gracefully, log failures, move on.**

---

### Lesson #3: Fuzzy Matching is a Lifesaver

Column names WILL vary:
- `Acct_Num` vs. `Account Number`
- `DR` vs. `Debit_Amt`
- Typos: `Desciption` (missing 'r')

**Fuzzy matching handles all of this automatically.**

---

### Lesson #4: Validate EVERYTHING

**Don't assume source data is correct!**

We found:
- 2 months with trial balances out of balance (source errors)
- 47 duplicate files (different versions, which to use?)
- 18 completely empty files
- 6 files from wrong time period (FY2013 file in FY2014 folder)

**Automated validation caught all of these.** ✅

---

### Lesson #5: Parquet > Excel for Large Datasets

**Excel File:**
- Size: 487 MB
- Load time: 2 minutes
- Crashes Excel on older computers

**Parquet File:**
- Size: 89 MB (81% smaller!)
- Load time: 3 seconds
- Works instantly

**Bonus:** Parquet preserves data types perfectly (no "Excel converted my account numbers to dates" issues)

---

## The Long-Term Impact

### Year 1:
- Saved $50,000 on consultants
- Completed migration in 1 week vs. 8 months
- Promoted to Senior Analyst
- 15% raise
- Became team's "Python expert"

### Year 2:
- Used same scripts for quarterly data loads (4 times/year)
- Saved 32 hours/quarter = 128 hours/year
- Automated 12 other reports using similar techniques
- Total time saved: ~400 hours/year

### Year 3:
- Trained 8 team members in Python
- Team automated 30+ processes
- Finance department recognized as "most efficient" in org
- CFO presented our work at industry conference
- I got another promotion 🚀

---

## Your Turn

Facing a data migration project?

**Don't panic. You've got this.** 💪

**Step 1:** Inventory your files  
**Step 2:** Build a robust reader  
**Step 3:** Standardize column names  
**Step 4:** Consolidate  
**Step 5:** Validate  
**Step 6:** Export  

**Time Investment:** 1-2 weeks

**Payoff:** Priceless

---

## Try It Yourself

Want the complete migration scripts? [Download from GitHub](https://github.com/nev1111/blog-code-examples)

Have your own migration success story? Share it in the comments!

---

## Join the Discussion on Discord! 💬

Facing a data migration challenge? **Join our Discord** and get help from people who've been there!

👉 **[Join PANDAUDIT Discord Server](https://discord.gg/your-invite-link)**

---

*"The best time to learn Python was 5 years ago. The second best time is today." 🚀*
