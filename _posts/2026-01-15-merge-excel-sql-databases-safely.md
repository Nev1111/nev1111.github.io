---
layout: primer_post
title: "🔐 Merge Excel Lists with SQL Databases (The Safe Way)"
subtitle: "Got 500 account numbers in Excel? Pull from database WITHOUT SQL injection risks!"
tags: [python, pandas, sql, security, database, excel, automation]
comments: true
author: PANDAUDIT Team
---

## The Problem

You have a list of 500 account numbers in Excel. You need to pull data from your SQL database for those accounts.

**Bad approach:**
```python
# ⚠️ DANGEROUS - SQL Injection risk!
query = f"SELECT * FROM accounts WHERE account_id IN ({','.join(account_list)})"
```

**Professional approach:** Parameterized queries.

---

## The Secure Solution

```python
import pandas as pd
import pyodbc

# Load your Excel list
accounts = pd.read_excel('accounts.xlsx')['Account_ID'].tolist()

# Create safe parameterized query
placeholders = ','.join(['?'] * len(accounts))
query = f"""
    SELECT Account_ID, Name, Balance
    FROM Accounts
    WHERE Account_ID IN ({placeholders})
"""

# Execute safely with parameter binding
conn = pyodbc.connect('Driver={SQL Server};Server=MyServer;Database=MyDB;...')
results = pd.read_sql_query(query, conn, params=accounts)

# Merge back with original Excel data
final = pd.merge(
    pd.read_excel('accounts.xlsx'),
    results,
    on='Account_ID',
    how='left'
)

final.to_excel('accounts_with_data.xlsx', index=False)
```

---

## Why Parameterized Queries?

### 🔒 Security
- Prevents SQL injection attacks
- Safe even with untrusted input

### ⚡ Performance
- Database can cache execution plan
- Faster for repeated queries

### 🎯 Reliability
- Handles special characters automatically
- No quote escaping needed

---

## Handle Large Lists (10,000+ items)

```python
def query_in_batches(conn, table, column, values, batch_size=1000):
    """Query large lists in batches"""
    results = []
    
    for i in range(0, len(values), batch_size):
        batch = values[i:i+batch_size]
        placeholders = ','.join(['?'] * len(batch))
        query = f"SELECT * FROM {table} WHERE {column} IN ({placeholders})"
        
        batch_results = pd.read_sql_query(query, conn, params=batch)
        results.append(batch_results)
    
    return pd.concat(results, ignore_index=True)

# Use it:
large_results = query_in_batches(conn, 'Accounts', 'Account_ID', account_list)
```

---

## The Bottom Line

✅ Secure - No SQL injection risks  
✅ Fast - Handles thousands of IDs  
✅ Reliable - Automatic type handling  
✅ Professional - Production-ready code  

**Stop building SQL strings. Use parameters.** 🔒

---

*Part of the "From Excel Hell to Python Heaven" series.*
