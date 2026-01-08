---
layout: primer_post
title: "🎯 Handle Duplicates Like a Data Pro"
subtitle: "Duplicate member records breaking your count? Learn to detect, flag, and deduplicate data correctly for accurate analysis."
tags: [python, pandas, duplicates, data-quality, deduplication, data-cleaning]
comments: true
author: PANDAUDIT Team
---

## The Duplicate Disaster

Your boss asks: *"How many active members do we have?"*

You run a count: **1,247 members**

Your colleague runs the same count: **1,186 members**

**What happened?** Your data has duplicates, and you counted them. Your colleague deduplicated first.

**Worse:** Neither of you is confident which number is correct.

This post teaches you to handle duplicates professionally.

---

## The Problem: Why Duplicates Happen

### Common Causes:

1. **Multiple records per person:**
   - Member has multiple accounts
   - Data imported multiple times
   - Historical records mixed with current

2. **Data entry errors:**
   - Same person entered twice (typos in name/ID)
   - System generates duplicate IDs

3. **Merging datasets:**
   - Joining tables creates duplicate rows
   - Many-to-many relationships

---

## Solution 1: Detect Duplicates

### The Basics: `.duplicated()`

```python
import pandas as pd

# Sample data with duplicates
df = pd.DataFrame({
    'Member_ID': ['001', '001', '002', '003', '003', '003'],
    'Name': ['Alice', 'Alice', 'Bob', 'Charlie', 'Charlie', 'Charlie'],
    'Account_Type': ['Pension', 'TDA', 'Pension', 'Pension', 'TDA', '401k']
})

print("Original data:")
print(df)

# Find duplicate Member_IDs
is_duplicate = df.duplicated(subset='Member_ID', keep='first')

print("\nDuplicate flags:")
print(is_duplicate)
# Output: [False, True, False, False, True, True]
```

**What `keep` means:**
- `keep='first'` → First occurrence is NOT a duplicate
- `keep='last'` → Last occurrence is NOT a duplicate
- `keep=False` → ALL duplicates are flagged (including first)

---

## Solution 2: Remove Duplicates

### Method 1: Keep First Occurrence

```python
# Remove duplicates, keep first occurrence
df_deduped = df.drop_duplicates(subset='Member_ID', keep='first')

print("After deduplication:")
print(df_deduped)
```

**Output:**
```
  Member_ID     Name Account_Type
0       001    Alice      Pension
2       002      Bob      Pension
3       003  Charlie      Pension
```

### Method 2: Keep Last Occurrence (Most Recent)

Useful when later records have updated information:

```python
# Sort by date first, then keep last (most recent)
df_sorted = df.sort_values('Date')
df_deduped = df_sorted.drop_duplicates(subset='Member_ID', keep='last')
```

---

## Solution 3: Count Unique Members Correctly

### Problem: Count Each Member Only Once

```python
# Sample data: Some members have multiple accounts
df = pd.DataFrame({
    'Member_ID': ['001', '001', '002', '003', '003', '003'],
    'Account_Type': ['Pension', 'TDA', 'Pension', 'Pension', 'TDA', '401k'],
    'Balance': [50000, 10000, 30000, 40000, 5000, 15000]
})

# WRONG: Count all rows
total_rows = len(df)
print(f"Total rows: {total_rows}")  # 6 (WRONG!)

# CORRECT: Count unique members
unique_members = df['Member_ID'].nunique()
print(f"Unique members: {unique_members}")  # 3 (CORRECT!)

# ALSO CORRECT: Deduplicate first, then count
unique_members_v2 = len(df.drop_duplicates(subset='Member_ID'))
print(f"Unique members (method 2): {unique_members_v2}")  # 3 (CORRECT!)
```

---

## Solution 4: Flag First Occurrence Only

### For Reporting: Mark Duplicates for Review

```python
# Flag duplicates (but keep all rows)
df['is_duplicate'] = df.duplicated(subset='Member_ID', keep='first')
df['is_first_occurrence'] = ~df['is_duplicate']

# Convert to integer for counting (True=1, False=0)
df['count_me'] = df['is_first_occurrence'].astype(int)

print(df)
```

**Output:**
```
  Member_ID Account_Type is_duplicate  is_first_occurrence  count_me
0       001      Pension        False                 True         1
1       001          TDA         True                False         0
2       002      Pension        False                 True         1
3       003      Pension        False                 True         1
4       003          TDA         True                False         0
5       003         401k         True                False         0
```

**Now you can accurately count:**
```python
correct_count = df['count_me'].sum()
print(f"Total unique members: {correct_count}")  # 3
```

---

## Solution 5: Aggregate Duplicates Instead of Removing

### When You Want Total Balance Across All Accounts

```python
# Group by Member_ID and aggregate
member_summary = df.groupby('Member_ID').agg({
    'Balance': 'sum',
    'Account_Type': 'count'  # How many accounts
}).reset_index()

member_summary.columns = ['Member_ID', 'Total_Balance', 'Account_Count']

print(member_summary)
```

**Output:**
```
  Member_ID  Total_Balance  Account_Count
0       001          60000              2
1       002          30000              1
2       003          60000              3
```

---

## Real-World Example: Member Demographics Report

### Problem: Count Active Members by Age Group

```python
import pandas as pd

# Data with some duplicate member records
members = pd.DataFrame({
    'Member_ID': ['001', '001', '002', '003', '003'],
    'Name': ['Alice', 'Alice', 'Bob', 'Charlie', 'Charlie'],
    'Age': [45, 45, 52, 61, 61],
    'Status': ['Active', 'Active', 'Active', 'Active', 'Active']
})

# WRONG: Count without deduplication
age_groups_wrong = members.groupby('Age')['Member_ID'].count()
print("WRONG count (includes duplicates):")
print(age_groups_wrong)
# Age 45: 2 members (WRONG - Alice counted twice!)
# Age 61: 2 members (WRONG - Charlie counted twice!)

# CORRECT: Deduplicate first, then count
members_unique = members.drop_duplicates(subset='Member_ID')
age_groups_correct = members_unique.groupby('Age')['Member_ID'].count()
print("\nCORRECT count (deduplicated):")
print(age_groups_correct)
# Age 45: 1 member (Alice)
# Age 52: 1 member (Bob)
# Age 61: 1 member (Charlie)
```

---

## Advanced: Detect Near-Duplicates (Fuzzy Matching)

### Problem: Same Person, Slightly Different Names

```python
from fuzzywuzzy import fuzz

# Data with typos/variations
df = pd.DataFrame({
    'Member_ID': ['001', '002', '003', '004'],
    'Name': ['John Smith', 'Jon Smith', 'Jane Doe', 'Jane  Doe']  # Note variations
})

# Calculate similarity scores
def find_similar_names(df, threshold=90):
    similar_pairs = []
    
    for i in range(len(df)):
        for j in range(i+1, len(df)):
            name1 = df.iloc[i]['Name']
            name2 = df.iloc[j]['Name']
            similarity = fuzz.ratio(name1, name2)
            
            if similarity >= threshold:
                similar_pairs.append({
                    'Name1': name1,
                    'Name2': name2,
                    'Similarity': similarity
                })
    
    return pd.DataFrame(similar_pairs)

# Find similar names
similar = find_similar_names(df, threshold=85)
print("Potential duplicates:")
print(similar)
```

**Output:**
```
          Name1        Name2  Similarity
0    John Smith    Jon Smith          91
1      Jane Doe    Jane  Doe          95
```

---

## Bonus: Identify Completely Duplicate Rows

### When ALL columns match

```python
# Find rows that are 100% identical
completely_duplicate = df.duplicated()

print(f"Completely duplicate rows: {completely_duplicate.sum()}")

# Remove completely duplicate rows
df_unique = df.drop_duplicates()

print(f"Original: {len(df)} rows")
print(f"After removing duplicates: {len(df_unique)} rows")
```

---

## Production Pattern: Deduplication with Audit Trail

### Track What Was Removed

```python
import pandas as pd
from datetime import datetime

def deduplicate_with_audit(df, subset_cols, keep='first'):
    """
    Remove duplicates and create audit trail
    
    Args:
        df: DataFrame to deduplicate
        subset_cols: Column(s) to check for duplicates
        keep: Which duplicate to keep ('first', 'last')
    
    Returns:
        - Deduplicated DataFrame
        - Audit DataFrame (removed records)
    """
    
    # Mark duplicates
    df['is_duplicate'] = df.duplicated(subset=subset_cols, keep=keep)
    
    # Separate duplicates
    df_keep = df[~df['is_duplicate']].copy()
    df_removed = df[df['is_duplicate']].copy()
    
    # Add audit info
    df_removed['Removal_Date'] = datetime.now()
    df_removed['Removal_Reason'] = 'Duplicate record'
    
    # Clean up flag from kept records
    df_keep = df_keep.drop(columns=['is_duplicate'])
    
    print(f"✅ Deduplication complete:")
    print(f"   Original rows: {len(df)}")
    print(f"   Kept: {len(df_keep)}")
    print(f"   Removed: {len(df_removed)}")
    
    return df_keep, df_removed

# Usage
members_clean, members_removed = deduplicate_with_audit(
    members,
    subset_cols='Member_ID',
    keep='first'
)

# Export audit trail
members_removed.to_excel('Removed_Duplicates_Audit.xlsx', index=False)
```

---

## Cheat Sheet: Duplicate Operations

| Task | Code | Result |
|------|------|--------|
| Find duplicates | `df.duplicated()` | Boolean Series |
| Count duplicates | `df.duplicated().sum()` | Number |
| Remove duplicates | `df.drop_duplicates()` | Deduplicated DF |
| Keep last occurrence | `df.drop_duplicates(keep='last')` | Deduplicated DF |
| Count unique | `df['col'].nunique()` | Number |
| Get unique values | `df['col'].unique()` | Array |
| Flag first occurrence | `~df.duplicated(keep='first')` | Boolean Series |

---

## Common Pitfalls

### ❌ Pitfall 1: Forgetting to Deduplicate Before Counting

```python
# WRONG
total_members = len(df)

# CORRECT
total_members = df['Member_ID'].nunique()
```

### ❌ Pitfall 2: Using `unique()` on DataFrame Instead of Series

```python
# WRONG
df.unique()  # Error!

# CORRECT
df['Member_ID'].unique()
```

### ❌ Pitfall 3: Deduplicating Without Sorting First

```python
# If you want most recent record, sort first!
df = df.sort_values('Date', ascending=False)
df_deduped = df.drop_duplicates(subset='Member_ID', keep='first')
```

---

## Try It Yourself!

```python
import pandas as pd

# Create sample data with duplicates
members = pd.DataFrame({
    'Member_ID': ['A001', 'A001', 'A002', 'A003', 'A003', 'A003'],
    'Name': ['Alice', 'Alice', 'Bob', 'Charlie', 'Charlie', 'Charlie'],
    'Account': ['Pension', 'TDA', 'Pension', 'Pension', 'TDA', '401k'],
    'Balance': [50000, 10000, 30000, 40000, 5000, 15000]
})

print("Original data (6 rows):")
print(members)

# How many unique members?
print(f"\nUnique members: {members['Member_ID'].nunique()}")

# Deduplicate (keep first)
members_deduped = members.drop_duplicates(subset='Member_ID', keep='first')
print(f"\nAfter deduplication (keep first): {len(members_deduped)} rows")

# OR: Aggregate by member
member_totals = members.groupby('Member_ID')['Balance'].sum()
print("\nTotal balance per member:")
print(member_totals)
```

---

## Benefits

✅ **Accurate counts:** No more overcounting  
✅ **Data quality:** Identify and fix duplicate sources  
✅ **Audit trail:** Track what was removed  
✅ **Confidence:** Know your numbers are correct  
✅ **Professional:** Handle edge cases properly

---

## What's Next?

Master deduplication, then:
- **Reshape data** → [Read this post](/2026-01-19-reshape-data-melt-pivot-python)
- **Master data mapping** → [Read this post](/2026-01-17-master-data-mapping-classifications)
- **End-to-end workflow** → [Read this post](/2026-01-21-end-to-end-workflow-example)

---

## Your Turn!

**What duplicate challenges do you face?** Share in the comments!

**Found a tricky duplicate scenario?** We can help solve it!

---

**Tags:** #Python #Pandas #Duplicates #DataQuality #Deduplication #DataCleaning

---

*Part of the "Advanced Techniques" series. Handle duplicates with confidence!*
