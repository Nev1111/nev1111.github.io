---
layout: mystery
title: "The Case of the Disappearing Dollars"
mystery_number: 001
series: "Masha & Panda Mysteries"
difficulty_level: "beginner"
estimated_time: "15 minutes"
skills_covered: [data_validation, rounding_errors, pandas_groupby]
real_scenario: true
character_focus: "both"
date: 2025-08-23
categories: [mysteries, reconciliation]
tags: [pandas, python, month-end, rounding]
---

## The Case

It was another routine month-end at the accounting firm. Sarah had run all the usual reports, and everything seemed to balance perfectly—or so she thought. The general ledger showed $847,392.15 in total revenue, but when she pulled the detailed subledger report and summed it up manually in Excel, she got $847,391.98.

A difference of 17 cents. Not much, but in accounting, 17 cents might as well be $17,000. Every penny needed to account.

> **Masha**: "Ugh, I hate when this happens! It's probably just a stupid rounding error, but now we have to spend hours checking every single transaction. There has to be a pattern here somewhere."

Sarah started where she always did—spot-checking individual transactions against the source documents. Invoice #3847 for $1,249.33? Perfect match. Payment receipt #9921 for $847.66? Exact match. After an hour of manual checking, she'd verified dozens of transactions, and every single one was correct.

The clock showed 4:30 PM. Sarah's eyes were getting tired from staring at spreadsheets, and she still hadn't found the source of the 17-cent discrepancy. She was starting to wonder if she'd made an error in her manual Excel calculation.

> **Panda**: "You know, Masha, maybe we're thinking about this wrong. Instead of checking individual transactions, what if we looked at how the systems are calculating the totals? Sometimes the issue isn't with the data—it's with the method."

That's when Sarah had a realization. She remembered something from her systems training: the subledger system rounded each transaction to two decimal places before storing it, but the general ledger calculation engine actually carried more precision internally before doing a final rounding step.

She decided to test this theory by pulling the raw transaction data into Python and comparing the two calculation methods directly.

> **Masha**: "Oh! So it's not a mistake at all—it's two different rounding methods giving slightly different results! No wonder we couldn't find a 'wrong' transaction."
> 
> **Panda**: "Exactly! And now we know how to catch this in the future instead of spending hours on manual checking. Let's document this solution so the next person doesn't have to go through the same detective work."

The mystery was solved. The 17-cent difference wasn't an error—it was a predictable outcome of how the two systems handled precision differently. Sarah felt both relieved and slightly annoyed that she'd spent an hour on manual checking, but she'd learned something valuable about her systems.

## The Solution

Here's how to detect and analyze rounding differences with Python and pandas:

```python
import pandas as pd
import numpy as np

# Sample data showing the rounding issue
transactions = pd.DataFrame({
 'transaction_id': ['INV001', 'INV002', 'INV003', 'PAY001'],
 'amount': [100.555, 200.446, 150.667, 75.337]
})

print("Original transaction amounts:")
print(transactions)
print()

# Method 1: Round each transaction first, then sum (subledger approach)
transactions['rounded_individual'] = transactions['amount'].round(2)
individual_rounded_sum = transactions['rounded_individual'].sum()

print("Method 1 - Round individual transactions first:")
print(transactions[['transaction_id', 'amount', 'rounded_individual']])
print(f"Total after individual rounding: ${individual_rounded_sum:.2f}")
print()

# Method 2: Sum first, then round (general ledger approach) 
raw_sum = transactions['amount'].sum()
sum_then_round = round(raw_sum, 2)

print("Method 2 - Sum all transactions, then round:")
print(f"Raw sum: ${raw_sum:.6f}")
print(f"Total after sum rounding: ${sum_then_round:.2f}")
print()

# Show the difference
difference = abs(individual_rounded_sum - sum_then_round)
print("Analysis:")
print(f"Method 1 (Individual Round): ${individual_rounded_sum:.2f}")
print(f"Method 2 (Sum Then Round): ${sum_then_round:.2f}")
print(f"Difference: ${difference:.2f}")
print()

# Create validation report for documentation
validation_report = pd.DataFrame({
 'Calculation_Method': ['Individual Round First', 'Sum Then Round', 'Difference'],
 'Amount': [individual_rounded_sum, sum_then_round, difference]
})

print("Validation Report for Management:")
print(validation_report.to_string(index=False))
```

## Key Learning Points

- **Different rounding methods create legitimate differences**: When systems round at different stages, small discrepancies are expected and normal
- **Verify calculation methodology before assuming errors**: Understanding how your systems work prevents unnecessary investigation time 
- **Use Python to test theories quickly**: Rather than manual checking, data analysis can reveal systematic differences immediately
- **Document system behaviors for the team**: Recording these discoveries helps colleagues avoid the same time-consuming investigations
- **Precision vs. display**: Internal calculations often use more precision than what's displayed, leading to rounding differences

---

*Ready for your next mystery? Check out the [Masha & Panda Mystery Series](/mysteries) for more accounting adventures!*