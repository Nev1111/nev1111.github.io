---
layout: post
title: "Age Grouping & Binning for Actuarial Reports"
subtitle: "Create age brackets (5-year increments, <25, 90+) for pension, insurance, and HR reports. Math meets elegance."
tags: [python, pandas, age-grouping, binning, actuarial, demographics, HR-analytics]
comments: true
author: PANDAUDIT Team
---

## The Age Grouping Challenge

You need to create a demographic report showing member distribution:

- **Under 25**
- **25-29**
- **30-34**
- **35-39**
- ...
- **85-89**
- **90+**

In Excel, this requires:
- Massive nested IF statement, OR
- VLOOKUP to a range table, OR
- Manual categorization ()

In Python, it's **one line of elegant math**.

---

## Why Age Grouping Matters

### Common Use Cases:

1. **Pension & Actuarial:** 
 - Demographic distribution of active members
 - Benefit payment analysis by age cohort
 - Retirement projections

2. **HR & Benefits:** 
 - Healthcare cost analysis by age group
 - Compensation equity analysis
 - Succession planning

3. **Insurance:** 
 - Premium calculations
 - Risk assessment
 - Claims analysis

---

## Solution 1: Mathematical Binning (5-Year Increments)

### The Elegant Formula

```python
import pandas as pd
import numpy as np

# Sample data
df = pd.DataFrame({
 'Member_ID': ['001', '002', '003', '004', '005'],
 'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
 'Age': [27, 34, 42, 58, 73]
})

# Create age groups (5-year increments)
df['Age_Group'] = (np.floor(df['Age'] / 5) * 5).astype(int)

print(df[['Name', 'Age', 'Age_Group']])
```

**Output:**
```
 Name Age Age_Group
0 Alice 27 25
1 Bob 34 30
2 Charlie 42 40
3 Diana 58 55
4 Eve 73 70
```

**How It Works:**
- `df['Age'] / 5` → 27/5 = 5.4, 34/5 = 6.8
- `np.floor()` → 5.4 → 5, 6.8 → 6
- `* 5` → 5×5 = 25, 6×5 = 30

---

## Solution 2: pd.cut() for Custom Ranges

### More Control with `pd.cut()`

```python
# Define age brackets
bins = [0, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 150]
labels = ['<25', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', 
 '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90+']

df['Age_Bracket'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

print(df[['Name', 'Age', 'Age_Bracket']])
```

**Output:**
```
 Name Age Age_Bracket
0 Alice 27 25-29
1 Bob 34 30-34
2 Charlie 42 40-44
3 Diana 58 55-59
4 Eve 73 70-74
```

**Parameters Explained:**
- `bins` = Boundaries of each group
- `labels` = Names for each group
- `right=False` = Exclude right boundary (e.g., 25-29 means 25 ≤ age < 30)

---

## Solution 3: Custom Function for Special Rules

### When You Have Actuarial Standards

```python
def categorize_age(age):
 """
 Categorize age per actuarial reporting standards
 - Ages ≤ 25: '<= 25'
 - Ages 26-89: 5-year brackets
 - Ages ≥ 90: '90+'
 """
 if age <= 25:
 return '≤25'
 elif age >= 90:
 return '90+'
 else:
 # Round down to nearest 5
 base = (age // 5) * 5
 return f"{base}-{base+4}"

# Apply to dataframe
df['Age_Category'] = df['Age'].apply(categorize_age)

print(df[['Name', 'Age', 'Age_Category']])
```

**Output:**
```
 Name Age Age_Category
0 Alice 27 25-29
1 Bob 34 30-34
2 Charlie 42 40-44
3 Diana 58 55-59
4 Eve 73 70-74
```

---

## Real-World Example: Pension Member Demographics

### Complete Analysis Pipeline

```python
import pandas as pd
import numpy as np

# Load member data
members = pd.read_excel('active_members.xlsx')

print(f"Total members: {len(members):,}")

# Create age groups
members['Age_Group'] = (np.floor(members['Age'] / 5) * 5).astype(int)

# Handle special cases
members.loc[members['Age'] < 25, 'Age_Group'] = '<25'
members.loc[members['Age'] >= 90, 'Age_Group'] = '90+'

# Aggregate by age group
age_distribution = members.groupby('Age_Group').agg({
 'Member_ID': 'count',
 'Current_Salary': 'mean',
 'Years_of_Service': 'mean'
}).reset_index()

age_distribution.columns = ['Age_Group', 'Member_Count', 'Avg_Salary', 'Avg_Service_Years']

# Calculate percentages
age_distribution['Percent_of_Total'] = (
 age_distribution['Member_Count'] / age_distribution['Member_Count'].sum() * 100
).round(1)

print("\nAge Distribution Report:")
print(age_distribution)

# Export
age_distribution.to_excel('Age_Distribution_Report.xlsx', index=False)
```

**Output:**
```
 Age_Group Member_Count Avg_Salary Avg_Service_Years Percent_of_Total
0 <25 45 42,500.00 2.1 3.6
1 25 123 48,750.00 5.3 9.8
2 30 189 55,200.00 8.7 15.1
3 35 234 62,400.00 12.4 18.7
4 40 201 68,100.00 15.8 16.0
...
```

---

## Solution 4: Age Grouping for Benefit Payment Analysis

### Problem: Analyze Benefits Paid by Age Group

```python
# Data: Monthly benefit payments
payments = pd.read_excel('benefit_payments.xlsx')

# Create age groups
payments['Age_Group'] = (np.floor(payments['Age'] / 5) * 5).astype(int)

# Aggregate by age group
benefit_summary = payments.groupby('Age_Group').agg({
 'Member_ID': 'nunique', # Unique members
 'Benefit_Amount': ['sum', 'mean', 'median']
}).reset_index()

# Flatten multi-level columns
benefit_summary.columns = ['Age_Group', 'Member_Count', 'Total_Benefits', 'Avg_Benefit', 'Median_Benefit']

print("Benefits by Age Group:")
print(benefit_summary)
```

---

## Solution 5: Create Pivot Table by Age Group

### Multi-Dimensional Analysis

```python
# Pivot: Age groups vs. Gender
age_gender_pivot = members.pivot_table(
 index='Age_Group',
 columns='Gender',
 values='Member_ID',
 aggfunc='count',
 fill_value=0
)

age_gender_pivot['Total'] = age_gender_pivot.sum(axis=1)

print("Member Distribution by Age Group and Gender:")
print(age_gender_pivot)
```

**Output:**
```
Age_Group Female Male Total
<25 23 22 45
25 65 58 123
30 102 87 189
35 125 109 234
...
```

---

## Bonus: Visualize Age Distribution

### Quick Histogram

```python
import matplotlib.pyplot as plt

# Create histogram
members.groupby('Age_Group')['Member_ID'].count().plot(kind='bar')
plt.title('Member Distribution by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Number of Members')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('age_distribution.png')
print(" Chart saved as age_distribution.png")
```

---

## Advanced: Custom Bin Width

### Not Always 5-Year Groups

```python
def create_age_bins(df, bin_width=10):
 """Create age groups with custom bin width"""
 
 min_age = df['Age'].min()
 max_age = df['Age'].max()
 
 # Generate bins
 bins = list(range(0, int(max_age) + bin_width, bin_width))
 
 # Generate labels
 labels = [f"{b}-{b+bin_width-1}" for b in bins[:-1]]
 
 df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
 
 return df

# Use 10-year groups
members_10yr = create_age_bins(members, bin_width=10)

print(members_10yr.groupby('Age_Group')['Member_ID'].count())
```

---

## Comparison: Excel vs. Python

### Excel Nested IF Approach:

```excel
=IF(A2<=25,"≤25",
 IF(A2<30,"25-29",
 IF(A2<35,"30-34",
 IF(A2<40,"35-39",
 IF(A2<45,"40-44",
 IF(A2<50,"45-49",
 IF(A2<55,"50-54",
 IF(A2<60,"55-59",
 IF(A2<65,"60-64",
 IF(A2<70,"65-69",
 IF(A2<75,"70-74",
 IF(A2<80,"75-79",
 IF(A2<85,"80-84",
 IF(A2<90,"85-89","90+"))))))))))))))
```

**Line count:** 1 formula, ~400 characters 
**Maintainability:** Nightmare 
**Performance:** Slow on 10,000+ rows

### Python Mathematical Approach:

```python
df['Age_Group'] = (np.floor(df['Age'] / 5) * 5).astype(int)
```

**Line count:** 1 line 
**Maintainability:** Simple 
**Performance:** Instant on 100,000+ rows

---

## Common Age Grouping Patterns

| Pattern | Use Case | Code |
|---------|----------|------|
| 5-year brackets | Actuarial reports | `(np.floor(age/5) * 5)` |
| 10-year brackets | General demographics | `(np.floor(age/10) * 10)` |
| Custom ranges | Insurance risk tiers | `pd.cut(age, bins, labels)` |
| Quartiles | Statistical analysis | `pd.qcut(age, q=4)` |

---

## Try It Yourself!

```python
import pandas as pd
import numpy as np

# Create sample data
members = pd.DataFrame({
 'Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
 'Age': [23, 27, 34, 42, 67]
})

# Method 1: Mathematical
members['Age_Group_Math'] = (np.floor(members['Age'] / 5) * 5).astype(int)

# Method 2: pd.cut()
bins = [0, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 150]
labels = ['<25', '25-29', '30-34', '35-39', '40-44', '45-49', 
 '50-54', '55-59', '60-64', '65-69', '70+']
members['Age_Group_Cut'] = pd.cut(members['Age'], bins=bins, labels=labels, right=False)

print(members)

# Analyze
print("\nDistribution:")
print(members['Age_Group_Cut'].value_counts().sort_index())
```

---

## Benefits

 **Professional:** Actuarial-standard age groups 
 **Efficient:** One line vs. 400-character formula 
 **Flexible:** Easy to change bin size 
 **Scalable:** Handle 100,000+ records instantly 
 **Auditable:** Clear logic, no nested IFs

---

## What's Next?

Master age grouping, then:
- **Pivot table analysis** → [Read this post](/2026-01-12-pivot-tables-on-steroids-multi-level-analysis-in-one-line)
- **Demographic reporting** → Coming soon!
- **Statistical analysis** → Coming soon!

---

## Your Turn!

**What age grouping standards does your industry use?** Share in the comments!

**Need help with custom grouping logic?** Ask away!

---

**Tags:** #Python #Pandas #AgeGrouping #Binning #Actuarial #Demographics #HRAnalytics

---

*Part of the "Advanced Techniques" series. Group ages like a pro!*
