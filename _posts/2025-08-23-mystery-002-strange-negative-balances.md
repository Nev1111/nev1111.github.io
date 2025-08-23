---
layout: mystery
title: "The Case of the Strange Negative Balances"
mystery_number: 002
series: "Masha & Panda Mysteries"
difficulty_level: "beginner"
estimated_time: "10 minutes"
skills_covered: [data_cleaning, string_manipulation, legacy_systems]
real_scenario: true
character_focus: "both"
date: 2025-08-23
categories: [mysteries, data-cleaning]
tags: [pandas, legacy-systems, data-formatting, negative-balances]
previous_mystery: "/2025-08-23-mystery-001-disappearing-dollars/"
next_mystery: "/2025-08-23-mystery-003-time-traveling-addresses/"
---

## The Case

Sarah thought she was having a quiet Friday afternoon when the email landed in her inbox: "URGENT: Legacy system import failed - negative balances not recognized." 

The attachment contained an Excel file from the old mainframe system with what looked like normal accounting data. But something was very wrong. The system kept rejecting entries like "5,009-" and "69.35-" as invalid numbers.

> **Masha**: "Are you kidding me? What kind of ancient system puts the negative sign at the END of the number? This is going to mess up our entire month-end if we can't get these balances imported!"

Sarah opened the file and stared at the data. Sure enough, instead of normal negative numbers like "-5,009", the old system exported negative balances as "5,009-" and "8,959-". Some even had "CR" suffixes instead of the minus sign. The modern accounting software had no idea what to do with this bizarre formatting.

The clock was ticking. The month-end deadline was Monday morning, and they had thousands of these strange balance entries to process.

> **Panda**: "You know, Masha, this is actually pretty common with legacy mainframe systems. They were built decades ago when screen space was precious. Instead of spending extra character positions on a leading minus sign, they put it at the end. We just need to teach Python to understand their logic."

Sarah realized this wasn't just a one-time problem. Every month they'd be importing data from this legacy system until the company finally migrated everything. She needed a reliable way to convert these weird negative formats into proper numbers that modern systems could understand.

> **Masha**: "Okay, so we need to find every entry that ends with '-' or 'CR', flip it to a proper negative number, and clean up all those commas too. At least this is something Python can handle systematically."
> 
> **Panda**: "Exactly! Once we build the solution, we can use it every month without having to manually fix thousands of entries. Let me show you how pandas can make sense of this legacy formatting."

By the end of the afternoon, Sarah had a robust solution that could handle any combination of the old system's quirky negative formatting. Monday's deadline was saved, and she'd never have to manually convert legacy balances again.

## The Solution

Here's how to convert legacy negative balance formats to modern numeric values:

```python
import pandas as pd

# Sample data showing the legacy formatting issue
df = pd.DataFrame({
    'Amount': ['5,009-', '69.35-', '8,959-', '8,953.23', '10,520', '1,200CR', '500-']
})

print("Original legacy data:")
print(df)
print()

# Step 1: Create a mask to identify negative balances (ending with '-' or 'CR')
negative_mask = df['Amount'].str.endswith(('-', 'CR'))

print("Identifying negative entries:")
print(df[negative_mask])
print()

# Step 2: Clean up the negative entries
# Remove the trailing '-' or 'CR' and add a leading '-'
df.loc[negative_mask, 'Amount'] = '-' + df.loc[negative_mask, 'Amount'].str.replace(r'[-CR]+$', '', regex=True)

print("After fixing negative signs:")
print(df)
print()

# Step 3: Remove commas from all entries
df['Amount'] = df['Amount'].str.replace(',', '')

print("After removing commas:")
print(df)
print()

# Step 4: Convert to numeric values
df['Amount'] = pd.to_numeric(df['Amount'])

print("Final cleaned data:")
print(df)
print()

# Verify the data types and values
print("Data type:", df['Amount'].dtype)
print("Sum of all amounts:", df['Amount'].sum())

# Create a summary report
summary = pd.DataFrame({
    'Metric': ['Total Entries', 'Negative Entries', 'Positive Entries', 'Net Amount'],
    'Value': [
        len(df),
        (df['Amount'] < 0).sum(),
        (df['Amount'] > 0).sum(),
        df['Amount'].sum()
    ]
})

print("\nLegacy Import Summary:")
print(summary.to_string(index=False))
```

## Key Learning Points

- **Legacy systems often have unconventional formatting**: Understanding older system conventions helps with data migration projects
- **String methods are powerful for data cleaning**: Use `.str.endswith()`, `.str.replace()` with regex for pattern matching
- **Systematic approach prevents errors**: Create masks to identify problematic data before making changes
- **Always verify your transformations**: Check data types and run validation calculations after cleaning
- **Build reusable solutions**: Once you solve a legacy formatting issue, document it for future imports

---

*Ready for your next mystery? Check out the [Masha & Panda Mystery Series](/mysteries) for more accounting adventures!*