---
layout: post
title: "When Your Data Speaks Two Languages: Text Parsing Adventures"
subtitle: "Your legacy system exports gibberish. Here's how to make sense of it."
tags: [python, pandas, regex, text-parsing, legacy-systems, data-extraction]
comments: true
author: PANDAUDIT Team
---

## The Text File From Hell

Our Legacy Accounting System system exports look like this:

```
TRIAL BALANCE REPORT - ALL FUNDS
RUN DATE: 12/31/2024
PAGE 1 OF 47

1234567-12-123456 CASH - OPERATING FUND 
 Beginning Balance 1,234,567.89
 12/01/2024 GJ 001234 Monthly deposit 125,000.00
 12/05/2024 AP 005678 Vendor payment 15,234.56 CR
 12/15/2024 GJ 001289 Adjustment 500.00 CR
 Ending Balance 1,344,833.33

2345678-15-234567 INVESTMENTS - BOND FUND
 Beginning Balance 45,234,567.12
 12/10/2024 AI 002345 Interest income 234,567.89
 12/20/2024 GJ 001456 Transfer to operating 50,000.00 CR
 Ending Balance 45,419,135.01

...
```

**My Task:** Extract this into a clean dataset.

**Excel's Reaction:** "LOL, good luck!" 

---

## Why This Is Hard

### Problem #1: Mixed Data Structures

- **Header lines:** Account number + description
- **Summary lines:** "Beginning Balance", "Ending Balance"
- **Detail lines:** Date, reference, description, amount
- **Page headers:** Report title, run date, page numbers

**All in ONE column of text!** 

---

### Problem #2: No Delimiters

**CSV:** Comma-separated 
**TSV:** Tab-separated 
**This:** *Space-separated... sometimes?* 

```
1234567-12-123456 CASH - OPERATING FUND
 12/01/2024 GJ 001234 Monthly deposit 125,000.00
```

**Where does one field end and another begin?** *¯\\_(ツ)_/¯*

---

### Problem #3: Hierarchical Structure

**Account number appears ONCE**, but applies to all subsequent detail lines:

```
1234567-12-123456 CASH - OPERATING FUND <-- Header
 12/01/2024 ... <-- Detail (belongs to account above)
 12/05/2024 ... <-- Detail (belongs to account above)
 12/15/2024 ... <-- Detail (belongs to account above)
```

**How do you "fill down" the account number in Python?**

---

### Problem #4: Credit Notation

```
 15,234.56 CR
```

**Means:** -15,234.56

**But Python sees:** A string with "CR" at the end

---

### Problem #5: Inconsistent Spacing

Some lines have:
- 2 spaces between fields
- 4 spaces
- 10 spaces
- **Variable spacing** depending on field length

**Why?** Because Legacy Accounting System was designed for **fixed-width printing** on **dot matrix printers** in **1987**. ️

---

## The Excel Attempt (Spoiler: It's Painful)

### Step 1: Import as Text

**Data → From Text/CSV → Import**

**Result:** Everything in Column A

---

### Step 2: Text to Columns

**Data → Text to Columns → Delimited → Space**

**Result:** 47 columns of garbage

**Why?** Variable spacing means some rows have 5 "columns", some have 15.

---

### Step 3: Manual Parsing (The Truth)

What you ACTUALLY do:

1. Open in Excel
2. Manually scroll through 47 pages
3. Copy account numbers
4. Paste into new sheet
5. Copy amounts
6. Paste into new sheet
7. **Repeat for 2,847 accounts**
8. Drink heavily
9. Question career choices

**Time:** 6-8 hours ⏰

**Errors:** 20-30 (you're human)

**Sanity remaining:** 15% 

---

## The Python Way: Regex to the Rescue

### Pattern #1: Extract Account Numbers

**Account Format:** `1234567-12-123456` (7 digits, hyphen, 2 digits, hyphen, 6 digits)

```python
import pandas as pd
import re

# Read the text file
df = pd.read_table('trial_balance.txt', header=None, names=['raw'])

# Extract account number using regex
df['Account_Num'] = df['raw'].str.extract(r'(\d{7}\-\d{2}\-\d{6})')

# Forward fill to propagate account number down to detail rows
df['Account_Num'] = df['Account_Num'].ffill()
```

**Regex Breakdown:**
- `\d{7}` = Exactly 7 digits
- `\-` = Literal hyphen
- `\d{2}` = Exactly 2 digits
- `\-` = Literal hyphen
- `\d{6}` = Exactly 6 digits

**Result:**
```
raw Account_Num
1234567-12-123456 CASH - OPERATING FUND 1234567-12-123456
 Beginning Balance 1234567-12-123456 <-- Filled down!
 12/01/2024 GJ 001234 Monthly deposit 1234567-12-123456 <-- Filled down!
 12/05/2024 AP 005678 Vendor payment 1234567-12-123456 <-- Filled down!
```

**Magic!** 

---

### Pattern #2: Extract Account Description

**Pattern:** Account number, then 4+ spaces, then description

```python
# Extract description (everything after account number)
df['Account_Desc'] = df['raw'].str.extract(r'\d{7}\-\d{2}\-\d{6}\s{4,}(.*)')

# Forward fill
df['Account_Desc'] = df['Account_Desc'].ffill()
```

**Regex Breakdown:**
- `\d{7}\-\d{2}\-\d{6}` = Account number pattern
- `\s{4,}` = At least 4 spaces
- `(.*)` = Capture everything after (description)

---

### Pattern #3: Extract Transaction Dates

**Date Format:** `12/31/2024` (MM/DD/YYYY)

```python
# Extract dates
df['Transaction_Date'] = df['raw'].str.extract(r'(\d{2}/\d{2}/\d{4})')

# Convert to datetime
df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'], errors='coerce')
```

**Regex Breakdown:**
- `\d{2}/\d{2}/\d{4}` = MM/DD/YYYY format

**`errors='coerce'`**: If conversion fails, set to `NaT` (Not a Time) instead of erroring

---

### Pattern #4: Extract Amounts

**Amount Patterns:**
- `125,000.00` (normal)
- `15,234.56 CR` (credit)

```python
# Extract amounts (with optional CR suffix)
df['Amount'] = df['raw'].str.extract(r'([\d,]+\.\d{2}(?:\s+CR)?)')

# Handle credit notation
mask = df['Amount'].str.contains('CR', na=False)
df.loc[mask, 'Amount'] = '-' + df.loc[mask, 'Amount'].str.replace(' CR', '')

# Remove commas and convert to float
df['Amount'] = df['Amount'].str.replace(',', '').astype(float)
```

**Regex Breakdown:**
- `[\d,]+` = One or more digits or commas
- `\.` = Literal decimal point
- `\d{2}` = Exactly 2 decimal places
- `(?:\s+CR)?` = Optional space(s) + "CR"

---

### Pattern #5: Filter Detail Lines Only

**Problem:** Report contains:
- Header lines
- Page headers
- Summary lines ("Beginning Balance", "Ending Balance")
- Blank lines

**We only want detail lines** (with dates and amounts).

```python
# Keep only rows with transaction dates
detail_lines = df.dropna(subset=['Transaction_Date'])

# Alternatively: Filter by pattern
detail_lines = df[df['raw'].str.contains(r'\d{2}/\d{2}/\d{4}', na=False)]
```

---

## Putting It All Together

```python
import pandas as pd
import re

# Read raw text file
df = pd.read_table('trial_balance.txt', header=None, names=['raw'])

# Extract all fields using regex
df['Account_Num'] = df['raw'].str.extract(r'(\d{7}\-\d{2}\-\d{6})')
df['Account_Desc'] = df['raw'].str.extract(r'\d{7}\-\d{2}\-\d{6}\s{4,}(.*)')
df['Transaction_Date'] = df['raw'].str.extract(r'(\d{2}/\d{2}/\d{4})')
df['Amount'] = df['raw'].str.extract(r'([\d,]+\.\d{2}(?:\s+CR)?)')

# Forward fill account info (propagate header down to detail rows)
df['Account_Num'] = df['Account_Num'].ffill()
df['Account_Desc'] = df['Account_Desc'].ffill()

# Handle credit notation
mask = df['Amount'].str.contains('CR', na=False)
df.loc[mask, 'Amount'] = '-' + df.loc[mask, 'Amount'].str.replace(' CR', '')
df['Amount'] = df['Amount'].str.replace(',', '', regex=False)

# Convert data types
df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'], errors='coerce')
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

# Keep only detail lines (with dates)
detail_lines = df.dropna(subset=['Transaction_Date', 'Amount']).copy()

# Clean up
detail_lines = detail_lines[['Account_Num', 'Account_Desc', 'Transaction_Date', 'Amount']]

# Export
detail_lines.to_excel('trial_balance_clean.xlsx', index=False)

print(f"Extracted {len(detail_lines):,} transactions from {len(df)} lines")
```

**Result:**
```
Extracted 15,847 transactions from 24,539 lines
```

**Time:** 15 seconds 

**Errors:** Zero 

**Coffee consumed:** 1 cup (for enjoyment, not desperation)

---

## Real-World Example: Vendor Payment Report

### The Challenge

**Report Format:**
```
VENDOR PAYMENT DETAIL REPORT
FOR PERIOD: 01/01/2024 - 12/31/2024

Vendor: 12345 - ABC CONSTRUCTION INC
 Invoice: INV-2024-001 Date: 01/15/2024 Amount: $125,000.00
 Invoice: INV-2024-015 Date: 03/22/2024 Amount: $87,500.50
 Invoice: INV-2024-028 Date: 06/10/2024 Amount: $45,200.00
 Total Vendor: $257,700.50

Vendor: 67890 - XYZ CONSULTING LLC
 Invoice: 2024-A-0045 Date: 02/14/2024 Amount: $15,000.00
 Invoice: 2024-A-0089 Date: 05/30/2024 Amount: $22,500.00
 Total Vendor: $37,500.00

GRAND TOTAL: $295,200.50
```

**Task:** Extract all invoices with vendor info

---

### The Solution

```python
import pandas as pd

# Read report
df = pd.read_table('vendor_payments.txt', header=None, names=['raw'])

# Extract vendor number and name
df['Vendor_Num'] = df['raw'].str.extract(r'Vendor:\s+(\d+)')
df['Vendor_Name'] = df['raw'].str.extract(r'Vendor:\s+\d+\s+\-\s+(.*)')

# Extract invoice details
df['Invoice_Num'] = df['raw'].str.extract(r'Invoice:\s+(\S+)')
df['Invoice_Date'] = df['raw'].str.extract(r'Date:\s+(\d{2}/\d{2}/\d{4})')
df['Invoice_Amount'] = df['raw'].str.extract(r'Amount:\s+\$([\d,]+\.\d{2})')

# Forward fill vendor info
df['Vendor_Num'] = df['Vendor_Num'].ffill()
df['Vendor_Name'] = df['Vendor_Name'].ffill()

# Convert data types
df['Invoice_Date'] = pd.to_datetime(df['Invoice_Date'], errors='coerce')
df['Invoice_Amount'] = df['Invoice_Amount'].str.replace(',', '').astype(float)

# Keep only invoice detail lines
invoices = df.dropna(subset=['Invoice_Num']).copy()
invoices = invoices[['Vendor_Num', 'Vendor_Name', 'Invoice_Num', 'Invoice_Date', 'Invoice_Amount']]

print(invoices)
```

**Output:**
```
 Vendor_Num Vendor_Name Invoice_Num Invoice_Date Invoice_Amount
0 12345 ABC CONSTRUCTION INC INV-2024-001 2024-01-15 125000.00
1 12345 ABC CONSTRUCTION INC INV-2024-015 2024-03-22 87500.50
2 12345 ABC CONSTRUCTION INC INV-2024-028 2024-06-10 45200.00
3 67890 XYZ CONSULTING LLC 2024-A-0045 2024-02-14 15000.00
4 67890 XYZ CONSULTING LLC 2024-A-0089 2024-05-30 22500.00
```

**Perfect!** 

---

## Common Text Parsing Patterns

### Pattern #1: Extract Specific Fields

```python
# Extract account number (fixed format)
df['Account'] = df['text'].str.extract(r'(\d{7}\-\d{2}\-\d{6})')

# Extract dollar amounts
df['Amount'] = df['text'].str.extract(r'\$?([\d,]+\.\d{2})')

# Extract dates (MM/DD/YYYY)
df['Date'] = df['text'].str.extract(r'(\d{2}/\d{2}/\d{4})')

# Extract email addresses
df['Email'] = df['text'].str.extract(r'([\w\.-]+@[\w\.-]+\.\w+)')
```

---

### Pattern #2: Forward Fill Headers

```python
# Extract header value (appears once per group)
df['Header'] = df['text'].str.extract(r'HEADER:\s+(.*)')

# Propagate down to all detail rows
df['Header'] = df['Header'].ffill()
```

---

### Pattern #3: Filter by Pattern

```python
# Keep only rows that contain dates
df_dates = df[df['text'].str.contains(r'\d{2}/\d{2}/\d{4}', na=False)]

# Keep only rows that start with a number
df_nums = df[df['text'].str.match(r'^\d', na=False)]

# Exclude header/footer lines
df_clean = df[~df['text'].str.contains(r'PAGE|TOTAL|REPORT', case=False, na=False)]
```

---

### Pattern #4: Split into Multiple Columns

```python
# Split on multiple spaces (2 or more)
df[['Col1', 'Col2', 'Col3']] = df['text'].str.split(r'\s{2,}', expand=True)

# Split on any delimiter
df[['First', 'Last']] = df['Name'].str.split(',', expand=True)
```

---

## Regex Cheat Sheet for Accountants

### Common Patterns

| Pattern | Regex | Example Match |
|---------|-------|---------------|
| **Account Number** | `\d{7}-\d{2}-\d{6}` | 1234567-12-123456 |
| **Dollar Amount** | `\$?[\d,]+\.\d{2}` | $1,234.56 |
| **Date (MM/DD/YYYY)** | `\d{2}/\d{2}/\d{4}` | 12/31/2024 |
| **Invoice Number** | `INV-\d{4}-\d{3}` | INV-2024-001 |
| **Credit Notation** | `[\d,]+\.\d{2}\s+CR` | 1,234.56 CR |
| **Email** | `[\w.-]+@[\w.-]+\.\w+` | user@example.com |
| **Phone Number** | `\d{3}-\d{3}-\d{4}` | 555-123-4567 |
| **SSN** | `\d{3}-\d{2}-\d{4}` | 123-45-6789 |
| **ZIP Code** | `\d{5}(-\d{4})?` | 12345 or 12345-6789 |

### Special Characters

| Character | Meaning | Example |
|-----------|---------|----------|
| `\d` | Any digit (0-9) | `\d{4}` = 4 digits |
| `\w` | Any word character (A-Z, a-z, 0-9, _) | `\w+` = one or more word chars |
| `\s` | Any whitespace (space, tab, newline) | `\s{2,}` = 2+ spaces |
| `.` | Any character (except newline) | `.*` = anything |
| `^` | Start of string | `^Invoice` = starts with "Invoice" |
| `$` | End of string | `CR$` = ends with "CR" |
| `*` | Zero or more | `\d*` = zero or more digits |
| `+` | One or more | `\d+` = one or more digits |
| `?` | Zero or one (optional) | `\$?` = optional dollar sign |
| `{n}` | Exactly n times | `\d{7}` = exactly 7 digits |
| `{n,}` | At least n times | `\s{2,}` = at least 2 spaces |
| `{n,m}` | Between n and m times | `\d{3,5}` = 3 to 5 digits |
| `[abc]` | Any character in set | `[ABC]` = A, B, or C |
| `[^abc]` | Any character NOT in set | `[^0-9]` = not a digit |
| `\|` | OR | `cat\|dog` = "cat" or "dog" |
| `()` | Capture group | `(\d{4})` = capture 4 digits |

---

## Testing Your Regex

Before running on 50,000 lines, **test on a few examples**:

```python
import re

# Test pattern
pattern = r'(\d{7}\-\d{2}\-\d{6})'
test_strings = [
 '1234567-12-123456 CASH ACCOUNT',
 'No account number here',
 ' Beginning Balance',
 '9876543-01-987654 INVESTMENT ACCOUNT'
]

for s in test_strings:
 match = re.search(pattern, s)
 if match:
 print(f"MATCH: {match.group(1)}")
 else:
 print(f"NO MATCH: {s}")
```

**Output:**
```
MATCH: 1234567-12-123456
NO MATCH: No account number here
NO MATCH: Beginning Balance
MATCH: 9876543-01-987654
```

**Perfect!** Regex is working as expected. 

---

## The "Aha!" Moment

**Coworker:** "How long did it take you to parse the trial balance?"

**Me:** "About 15 seconds."

**Coworker:** "No, I mean the WHOLE trial balance. All 24,000 lines."

**Me:** "Yeah. 15 seconds."

**Coworker:** *suspicious* "It takes me 6 hours to do it manually..."

**Me:** "Want me to show you?"

**30 minutes later:**

**Coworker:** "This is... life-changing. Can you teach the whole team?"

**Me:** "Already scheduled a workshop for next Friday."

**That Friday:** 12 people showed up (including the CFO)

**Two weeks later:** The team had automated 15 different legacy reports

**One month later:** We reclaimed 80 hours/month of manual data entry

**My career:** Never the same. 

---

## Common Pitfalls (And How to Avoid Them)

### Pitfall #1: Greedy Matching

**Problem:** `.*` matches TOO MUCH

```python
# BAD: Greedy match
pattern = r'Invoice: (.*) Date:'
# Matches: "INV-001 Date: 01/15/2024 Amount: $1,000 Date:" (too much!)

# GOOD: Non-greedy match
pattern = r'Invoice: (.*?) Date:'
# Matches: "INV-001" (stops at first "Date:")
```

---

### Pitfall #2: Forgetting to Escape Special Characters

```python
# BAD: Dot matches ANY character
pattern = r'\d.\d' # Matches "1X2", "1 2", "1.2"

# GOOD: Escaped dot matches literal period
pattern = r'\d\.\d' # Matches only "1.2"
```

---

### Pitfall #3: Not Handling Missing Data

```python
# BAD: Crashes if pattern not found
df['Amount'] = df['text'].str.extract(r'(\$[\d,]+\.\d{2})')
df['Amount'] = df['Amount'].astype(float) # ERROR on NaN values

# GOOD: Handle missing gracefully
df['Amount'] = df['text'].str.extract(r'(\$[\d,]+\.\d{2})')
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce') # NaN for missing
```

---

## The Bottom Line

**Legacy Systems Speak in Text.**

Your job: Translate it into clean data.

**Excel:** Manual, slow, error-prone

**Python + Regex:** Automated, fast, accurate

**Your Choice.** 

---

## Try It Yourself

Want the complete working examples? [Download from GitHub](https://github.com/nev1111/blog-code-examples)

Have a legacy system horror story? Share it in the comments!

---

## Join the Discussion on Discord! -

Stuck parsing a gnarly text file? **Join our Discord** and get help from the community!

 **[Join PANDAUDIT Discord Server](https://discord.gg/your-invite-link)**

---

*Next time: "5-Minute Fix: Stop Manually Counting Trading Days" →*
