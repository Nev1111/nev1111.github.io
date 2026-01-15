---
layout: page
title: Data Analytics Quick Reference
subtitle: Essential commands for accounting data analysis with Python and pandas
permalink: /cheatsheet/
---

### Data Analytics Quick Reference

*Your go-to guide for data analytics in accounting - featuring pandas/Python implementations*

---

#### Getting Started - Data Setup

| Task | Pandas Command | Example |
|------|----------------|---------|
| **Load CSV file** | `pd.read_csv()` | `df = pd.read_csv('transactions.csv')` |
| **Load Excel file** | `pd.read_excel()` | `df = pd.read_excel('ledger.xlsx', sheet_name='GL')` |
| **First look at data** | `df.head()` | `df.head(10) # First 10 rows` |
| **Data shape** | `df.shape` | `df.shape # (rows, columns)` |
| **Column info** | `df.info()` | Shows data types and null counts |
| **Quick stats** | `df.describe()` | Summary statistics for numeric columns |

---

#### Investigation Basics - Excel to Pandas

| Excel Function | Pandas Equivalent | Example |
|----------------|-------------------|-------------------|
| **VLOOKUP** | `merge()` | `df.merge(vendor_df, on='vendor_id')` |
| **Pivot Table** | `pivot_table()` | `df.pivot_table(values='amount', index='account', aggfunc='sum')` |
| **Filter** | `df[condition]` | `df[df['amount'] > 10000] # Large transactions` |
| **SUMIFS** | `groupby().sum()` | `df.groupby('department')['amount'].sum()` |
| **COUNTIFS** | `groupby().count()` | `df.groupby('account')['transaction_id'].count()` |
| **Remove Duplicates** | `drop_duplicates()` | `df.drop_duplicates(['date', 'amount', 'vendor'])` |
| **Sort** | `sort_values()` | `df.sort_values('date', ascending=False)` |
| **IF Formula** | `np.where()` | `df['flag'] = np.where(df['amount'] < 0, 'Credit', 'Debit')` |

---

#### Advanced Analysis Techniques

##### Data Quality Investigation
```python
# Find missing values
df.isna().sum() # Count missing per column
df[df.isna().any(axis=1)] # Rows with any missing data
df.dropna() # Remove rows with missing values
df.fillna(0) # Fill missing with zeros

# Spot duplicates
df.duplicated().sum() # Count duplicates
df[df.duplicated(keep=False)] # Show all duplicate rows
df.drop_duplicates(keep='first') # Keep first occurrence
```

##### Pattern Recognition
```python
# Text contains investigation
df[df['description'].str.contains('fraud', case=False)] # Find fraud mentions
df['description'].str.extract(r'(\$[\d,]+)') # Extract dollar amounts
df['account'].str.startswith('5') # Accounts starting with 5

# Date analysis
df['month'] = df['date'].dt.month # Extract month
df['quarter'] = df['date'].dt.quarter # Extract quarter
df[df['date'].between('2023-01-01', '2023-12-31')] # Date range filter
```

##### Reconciliation Techniques
```python
# Merge techniques
pd.merge(df1, df2, on='id', how='left') # Left join
pd.merge(df1, df2, on='id', how='outer', indicator=True) # Show merge status
pd.merge_asof(df1, df2, on='date', by='customer') # Nearest date match

# Set operations (finding the difference)
set(df1['id']) - set(df2['id']) # IDs in df1 but not df2
df1[~df1['id'].isin(df2['id'])] # Rows not in df2
```

---

#### Accounting-Specific Analysis

##### Financial Analysis
```python
# Monthly summaries
df.groupby(df['date'].dt.to_period('M'))['amount'].sum()

# Running totals (bank reconciliation style)
df['running_total'] = df['amount'].cumsum()

# Percentage of total
df['pct_of_total'] = df['amount'] / df['amount'].sum() * 100

# Top N analysis
df.nlargest(10, 'amount') # Top 10 by amount
df.nsmallest(5, 'amount') # Bottom 5 by amount
```

##### Legacy System Cleanup
```python
# Fix negative formatting (common in older systems)
df['amount'] = df['amount'].str.replace(r'[-CR]+$', '', regex=True)
df.loc[df['amount'].str.endswith('-'), 'amount'] = '-' + df['amount'].str[:-1]

# Clean currency formatting
df['amount'] = df['amount'].str.replace('$', '').str.replace(',', '')
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

# Extract numbers from text
df['extracted'] = df['description'].str.extract(r'(\d+\.?\d*)')
```

---

#### Anomaly Detection Patterns

```python
# Benford's Law check (first digit analysis)
first_digits = df['amount'].astype(str).str[0]
first_digits.value_counts().sort_index()

# Round number bias
df[df['amount'] % 100 == 0] # Exactly divisible by 100
df[df['amount'].astype(str).str.endswith('00')] # Ends in 00

# Weekend transactions (unusual timing)
df[df['date'].dt.dayofweek >= 5] # Saturday/Sunday transactions

# Statistical outliers
Q1 = df['amount'].quantile(0.25)
Q3 = df['amount'].quantile(0.75)
IQR = Q3 - Q1
df[(df['amount'] < Q1 - 1.5*IQR) | (df['amount'] > Q3 + 1.5*IQR)]
```

---

#### Quick Visualizations

```python
# Visual analysis toolkit
df['amount'].hist(bins=20) # Distribution plot
df.groupby('account')['amount'].sum().plot(kind='bar') # Account totals
df['date'].value_counts().plot() # Transaction frequency
df.boxplot(column='amount', by='department') # Department comparison
```

---

#### One-Liner Power Moves

```python
# Quick wins for busy professionals
df.groupby('vendor')['amount'].agg(['count', 'sum', 'mean']) # Vendor analysis
df.assign(month=df['date'].dt.month).pivot_table('amount', 'account', 'month') # Monthly pivot
df.query('amount > 1000 and department == "IT"') # Multiple conditions
df.sample(100) # Random sample
df.drop_duplicates().reset_index(drop=True) # Clean duplicates & reset index
```

---

#### Data Export for Reports

```python
# Share your findings
df.to_csv('investigation_results.csv', index=False)
df.to_excel('audit_findings.xlsx', sheet_name='Summary', index=False)

# Multi-sheet Excel export
with pd.ExcelWriter('full_investigation.xlsx') as writer:
 summary_df.to_excel(writer, sheet_name='Summary', index=False)
 detail_df.to_excel(writer, sheet_name='Detail', index=False)
```

---

#### Pro Tips

**Performance Boosters:**
- Use `df.query()` instead of `df[df['col'] == value]` for complex conditions
- Chain operations: `df.groupby('x').sum().sort_values('y', ascending=False)`
- Use `pd.cut()` for binning amounts into ranges

**Memory Savers:**
- Use `pd.read_csv(chunksize=1000)` for huge files
- Convert text to categories: `df['category'] = df['category'].astype('category')`
- Use appropriate data types: `pd.to_numeric(downcast='integer')`

**Debugging Helpers:**
- `df.dtypes` - Check data types
- `df.memory_usage()` - Memory consumption 
- `df.nunique()` - Count unique values per column

---

#### Reference by Topic

- **Rounding Issues**: `df.round(2)` vs `round(df.sum(), 2)`
- **Legacy Formats**: `str.replace()` with regex patterns
- **Historical Matching**: `pd.merge_asof()` for time-based joins
- **Missing Data**: `isna()`, `fillna()`, `dropna()`
- **Text Extraction**: `str.extract()` with regex patterns
- **Nearest Matching**: `merge_asof()` with direction parameters

---

*Keep this reference handy during your data work. Need help with a specific challenge? Email us at hello@pandaudit.com*
