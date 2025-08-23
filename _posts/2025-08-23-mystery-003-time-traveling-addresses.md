---
layout: mystery
title: "The Case of the Time-Traveling Addresses"
mystery_number: 003
series: "Masha & Panda Mysteries"
difficulty_level: "intermediate"
estimated_time: "15 minutes"
skills_covered: [merge_asof, date_matching, historical_data]
real_scenario: true
character_focus: "both"
date: 2025-08-23
categories: [mysteries, data-merging]
tags: [pandas, merge_asof, datetime, historical-records]
previous_mystery: "/2025-08-23-mystery-002-strange-negative-balances/"
next_mystery: "/2025-08-23-mystery-004-vanishing-data/"
---

## The Case

The audit team was in panic mode. They needed to verify customer addresses as of December 31st for the year-end audit, but the address database was a mess of historical changes. Customer 101 had moved three times during the year, Customer 102 had changed addresses twice, and the auditors needed to know exactly where each customer lived on that specific cutoff date.

"This is impossible," muttered the audit manager, staring at spreadsheets full of customer moves. "How are we supposed to figure out which address was current for each person on December 31st when we have years of address changes?"

> **Masha**: "This is such a nightmare! We have customer names in one file, and then this massive historical address log with dozens of address changes per customer. How do we even begin to match these correctly by date?"

Sarah looked at the two datasets. The customer file was simple - just names and IDs. But the address history file was a time-traveling maze: Customer 101 lived at Oak Street until March, then moved to Pine Avenue in June, then switched to Maple Drive in September. Which address should they use for the December 31st cutoff?

Making it worse, some customers had moved just days before year-end, while others hadn't moved in years. The auditors needed the address that was active on December 31st - not the newest address, not the oldest one, but the one that was current on that exact date.

> **Panda**: "You know, Masha, this is exactly what `merge_asof` was designed for. It's like a time machine for data - we can tell it to find the most recent address that was effective on or before our cutoff date. No manual date checking required."

Sarah realized this wasn't just about addresses. Every audit had these "point-in-time" requirements: What was the customer's credit limit on June 30th? Which vendor contract was active during Q3? What tax rate applied to this transaction on that specific date?

> **Masha**: "So instead of trying to manually check every address change date, we can let pandas do the time traveling for us? It'll automatically find the right historical record for each customer based on our cutoff date?"
> 
> **Panda**: "Exactly! We sort the historical data by date, then `merge_asof` works backwards from our cutoff date to find the most recent address that was effective. It's like having an assistant who can instantly look up what was true at any point in time."

By the end of the day, Sarah had a solution that could instantly generate point-in-time snapshots for any date. The auditors got their December 31st addresses, and Sarah knew she could handle any future "as of" date requests with confidence.

## The Solution

Here's how to match historical records to a specific point in time using merge_asof:

```python
import pandas as pd
from datetime import datetime

# Customer master file
customers = pd.DataFrame({
    'ID': [101, 102, 103],
    'Name': ['Alice Johnson', 'Bob Smith', 'Carol Davis']
})

# Historical address changes (multiple addresses per customer over time)
address_history = pd.DataFrame({
    'ID': [101, 101, 101, 102, 102, 103, 103],
    'Address': [
        '123 Oak Street', '456 Pine Avenue', '789 Maple Drive',
        '321 Elm Road', '654 Cedar Lane', 
        '987 Birch Way', '147 Spruce Court'
    ],
    'Effective_Date': [
        '2023-01-01', '2023-06-15', '2023-09-10',
        '2023-03-20', '2023-11-05',
        '2023-02-14', '2023-08-30'
    ]
})

print("Customer Master File:")
print(customers)
print("\nHistorical Address Changes:")
print(address_history)
print()

# Step 1: Convert the Effective_Date to datetime
address_history['Effective_Date'] = pd.to_datetime(address_history['Effective_Date'])

# Step 2: Sort by ID and Effective_Date (required for merge_asof)
address_history = address_history.sort_values(['ID', 'Effective_Date'])

print("Address history sorted by ID and date:")
print(address_history)
print()

# Step 3: Set our cutoff date (point-in-time we want)
cutoff_date = pd.to_datetime('2023-12-31')

# Step 4: Create a temporary dataframe with customers and cutoff date
customers_with_date = customers.copy()
customers_with_date['Cutoff_Date'] = cutoff_date

print(f"Looking for addresses as of: {cutoff_date.strftime('%Y-%m-%d')}")
print()

# Step 5: Use merge_asof to find the most recent address for each customer
# that was effective on or before the cutoff date
result = pd.merge_asof(
    customers_with_date.sort_values('ID'),  # Left dataframe (sorted by key)
    address_history,                         # Right dataframe (already sorted)
    left_on='Cutoff_Date',                  # Date column in left dataframe
    right_on='Effective_Date',              # Date column in right dataframe  
    by='ID'                                 # Match on customer ID
)

print("Final Result - Customer addresses as of December 31, 2023:")
print(result[['ID', 'Name', 'Address', 'Effective_Date']])
print()

# Let's also show what happens with different cutoff dates
cutoff_dates = ['2023-05-01', '2023-08-01', '2023-12-31']

print("Address lookup for different cutoff dates:")
for date_str in cutoff_dates:
    cutoff = pd.to_datetime(date_str)
    customers_temp = customers.copy()
    customers_temp['Cutoff_Date'] = cutoff
    
    temp_result = pd.merge_asof(
        customers_temp.sort_values('ID'),
        address_history,
        left_on='Cutoff_Date',
        right_on='Effective_Date',
        by='ID'
    )
    
    print(f"\nAs of {date_str}:")
    for _, row in temp_result.iterrows():
        print(f"  {row['Name']}: {row['Address']} (effective {row['Effective_Date'].strftime('%Y-%m-%d')})")
```

## Key Learning Points

- **merge_asof is perfect for point-in-time analysis**: Use it when you need to match historical records to a specific date
- **Data must be sorted for merge_asof**: Both dataframes need to be sorted by the date column (and by key if using multiple keys)
- **"As of" means "on or before"**: merge_asof finds the most recent record that was effective on or before your cutoff date
- **Works with any time-based data**: Credit limits, contract terms, tax rates, organization structures - any data that changes over time
- **Eliminates manual date checking**: No more complex loops or conditional logic to find the right historical record
- **Handles missing data gracefully**: If no record exists before the cutoff date, merge_asof returns NaN rather than throwing an error

---

*Ready for your next mystery? Check out the [Masha & Panda Mystery Series](/mysteries) for more accounting adventures!*