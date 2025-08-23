---
layout: mystery
title: "The Case of the Buried Treasure"
mystery_number: 005
series: "Masha & Panda Mysteries"
difficulty_level: "intermediate"
estimated_time: "12 minutes"
skills_covered: [regex, text_extraction, data_parsing]
real_scenario: true
character_focus: "both"
date: 2025-08-23
categories: [mysteries, text-processing]
tags: [pandas, regex, text-extraction, dollar-amounts]
previous_mystery: "/2025-08-23-mystery-004-vanishing-data/"
next_mystery: "/2025-08-23-mystery-006-the-closest-match/"
---

## The Case

The insurance claim report landed on Sarah's desk with a note: "Need total claim amounts ASAP for board meeting." She opened the file expecting a nice, clean spreadsheet with amounts in dedicated columns. Instead, she found a nightmare of unstructured text.

"Customer reported theft of laptop valued at $2,500 and iPhone worth $800 from vehicle..." read one entry. Another claimed "Damaged equipment includes printer ($1,200), monitor ($350), and software licenses totaling $4,500." 

Every claim was buried in paragraphs of narrative text with dollar amounts scattered throughout like hidden treasure.

> **Masha**: "You've got to be kidding me! They want me to manually hunt through hundreds of these text blobs, find every dollar amount, and add them up? This could take all day, and I'll probably miss half of them!"

Sarah stared at the document. Some amounts were written as "$2,500", others as "$1,200.00", and some even appeared as "two thousand five hundred dollars ($2,500)". The formatting was completely inconsistent, but she needed to extract every single dollar amount for the insurance summary.

The board meeting was in three hours. There were 847 claim descriptions, and each one contained multiple dollar amounts buried in the narrative text. Manual extraction would take days, not hours.

> **Panda**: "You know, Masha, this is exactly what regular expressions were invented for. We can create a pattern that finds any text that looks like a dollar amount, no matter how it's formatted in the sentence. It's like having X-ray vision for numbers."

Sarah realized this wasn't just about today's insurance report. The company regularly received unstructured documents - legal contracts with embedded costs, vendor emails with pricing scattered throughout, customer complaints mentioning refund amounts. All treasure troves of buried numerical data.

> **Masha**: "So instead of reading every single paragraph like a human, we can teach the computer to scan for patterns and extract just the dollar amounts? Like a metal detector for money mentions?"
> 
> **Panda**: "Exactly! Regular expressions can spot patterns like '$' followed by numbers, with or without commas and decimals. Once we extract all the amounts, we can analyze them just like any other numerical data. No more treasure hunting through text!"

Within an hour, Sarah had extracted 2,147 individual dollar amounts from the claim narratives, automatically categorized them by claim, and generated the summary report the board needed. The hidden treasure was finally revealed.

## The Solution

Here's how to extract dollar amounts from unstructured text using regular expressions:

```python
import pandas as pd
import re

# Sample unstructured text containing dollar amounts
claims_data = pd.DataFrame({
    'Claim_ID': [1001, 1002, 1003, 1004],
    'Description': [
        "Customer reported theft of laptop valued at $2,500 and iPhone worth $800 from vehicle on Main Street.",
        "Fire damage to office equipment including printer ($1,200), monitor ($350), and software licenses totaling $4,500.",
        "Water damage claim for $12,000.50 covering furniture replacement and $850 in cleaning services.",
        "Vehicle accident resulting in repairs estimated at $8,750 with additional rental car costs of $450.00."
    ]
})

print("Original Claims Data:")
print(claims_data)
print()

# Step 1: Define regex pattern to find dollar amounts
# Pattern explanation:
# \$ - literal dollar sign
# (?:\d{1,3}(?:,\d{3})*|\d+) - numbers with optional commas (1,000 or 1000)
# (?:\.\d{2})? - optional decimal part (.50)
dollar_pattern = r'\$(?:\d{1,3}(?:,\d{3})*|\d+)(?:\.\d{2})?'

# Step 2: Extract all dollar amounts from each description
def extract_dollar_amounts(text):
    """Extract all dollar amounts from text and return as list"""
    matches = re.findall(dollar_pattern, text)
    return matches

# Apply extraction to each row
claims_data['Dollar_Amounts_Found'] = claims_data['Description'].apply(extract_dollar_amounts)

print("Dollar amounts found in each claim:")
print(claims_data[['Claim_ID', 'Dollar_Amounts_Found']])
print()

# Step 3: Convert extracted amounts to numeric values
def clean_dollar_amount(amount_str):
    """Convert '$1,200.50' to 1200.50"""
    # Remove $ and commas, convert to float
    return float(amount_str.replace('$', '').replace(',', ''))

# Step 4: Calculate total for each claim
def calculate_claim_total(amounts_list):
    """Sum all dollar amounts in the list"""
    if not amounts_list:  # Handle empty lists
        return 0.0
    return sum(clean_dollar_amount(amount) for amount in amounts_list)

claims_data['Total_Amount'] = claims_data['Dollar_Amounts_Found'].apply(calculate_claim_total)

print("Claims with extracted totals:")
print(claims_data[['Claim_ID', 'Total_Amount']])
print()

# Step 5: Create detailed breakdown
detailed_breakdown = []
for _, row in claims_data.iterrows():
    claim_id = row['Claim_ID']
    for amount_str in row['Dollar_Amounts_Found']:
        detailed_breakdown.append({
            'Claim_ID': claim_id,
            'Amount_Text': amount_str,
            'Amount_Numeric': clean_dollar_amount(amount_str)
        })

breakdown_df = pd.DataFrame(detailed_breakdown)

print("Detailed breakdown of all extracted amounts:")
print(breakdown_df)
print()

# Step 6: Generate summary report
summary_stats = pd.DataFrame({
    'Metric': [
        'Total Claims Processed',
        'Total Dollar Amounts Found', 
        'Average Amounts per Claim',
        'Total Value of All Claims',
        'Largest Single Amount',
        'Smallest Single Amount'
    ],
    'Value': [
        len(claims_data),
        len(breakdown_df),
        round(len(breakdown_df) / len(claims_data), 1),
        f"${breakdown_df['Amount_Numeric'].sum():,.2f}",
        f"${breakdown_df['Amount_Numeric'].max():,.2f}",
        f"${breakdown_df['Amount_Numeric'].min():,.2f}"
    ]
})

print("Insurance Claims Summary Report:")
print(summary_stats.to_string(index=False))
print()

# Step 7: Show regex pattern testing
print("Testing regex pattern with various formats:")
test_amounts = [
    "$1,500", "$250.75", "$12,000.50", "$5", "$999,999.99", 
    "not money", "$0.99", "$1,234,567"
]

for test in test_amounts:
    matches = re.findall(dollar_pattern, test)
    print(f"'{test}' → Found: {matches}")
```

## Key Learning Points

- **Regular expressions are powerful for pattern matching**: Use regex to find consistent patterns in unstructured text, like dollar amounts
- **Design robust patterns**: Account for variations like commas, decimals, and different formatting styles in your regex
- **Extract first, then convert**: Pull the text patterns first, then clean and convert to numeric values for calculations
- **Handle edge cases**: Empty results, malformed amounts, and unusual formatting should be considered in your solution
- **Validate your regex**: Test your pattern against various examples to ensure it captures what you need and ignores what you don't
- **Unstructured data is everywhere**: Legal documents, emails, reports - many business documents hide valuable numerical data in text

---

*Ready for your next mystery? Check out the [Masha & Panda Mystery Series](/mysteries) for more accounting adventures!*