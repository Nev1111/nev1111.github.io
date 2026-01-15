---
layout: mystery
title: "The Case of the Closest Match"
mystery_number: 006
series: "Masha & Panda Mysteries"
difficulty_level: "advanced"
estimated_time: "18 minutes"
skills_covered: [merge_asof, nearest_match, complex_merging]
real_scenario: true
character_focus: "both"
date: 2025-08-23
categories: [mysteries, advanced-merging]
tags: [pandas, merge_asof, nearest-match, complex-joins]
previous_mystery: "/2025-08-23-mystery-005-buried-treasure/"
next_mystery: ""
---

## The Case

The investment portfolio reconciliation was turning into a nightmare. Sarah had two critical datasets: the portfolio holdings showing when each stock was purchased, and the market price history showing daily stock values. She needed to value each holding at its purchase date, but there was a problem.

"Look at this," Sarah said, pointing at her screen. "We bought Apple stock on March 15th, but the price history only has entries for March 14th and March 17th. There's no exact match for the purchase date."

The portfolio contained hundreds of stocks purchased on various dates throughout the year. The market data had daily prices, but not every single day - weekends were missing, holidays were skipped, and sometimes the data provider had gaps in their feed.

> **Masha**: "This is impossible! How are we supposed to value a stock purchased on March 15th when we only have prices for March 14th and March 17th? We can't just guess, and we can't leave gaps in our portfolio valuation!"

Sarah realized this wasn't just about missing dates. It was about finding the "nearest neighbor" in time. When she bought stock on March 15th, she needed the most recent price available - which would be March 14th, not the future price from March 17th.

But doing this manually for hundreds of holdings would take forever. She'd have to look up each purchase date, find the closest available price date that came before it, and manually match them up.

> **Panda**: "You know, Masha, this is exactly what `merge_asof` was designed for. It's like having a time-traveling assistant that can find the most recent available information as of any given date. No exact matches required."

Sarah started thinking about all the other scenarios where she needed "nearest match" logic: What was the employee's salary when they were promoted? What exchange rate was in effect when the international payment was made? What credit rating did the customer have when they applied for the loan?

> **Masha**: "So instead of hunting for exact date matches, we can tell pandas to find the closest available information? Like 'give me the most recent price before this purchase date, even if it's not exact'?"
> 
> **Panda**: "Exactly! It searches backwards through time to find the most recent information that was available when each transaction occurred. No more guessing, no more gaps, and no more manual lookup work."

By the end of the day, Sarah had a complete portfolio valuation with every holding properly priced using the nearest available market data. The reconciliation was complete, and she'd learned a powerful technique for handling imperfect real-world data.

## The Solution

Here's how to merge datasets when you need the closest match instead of exact matches:

```python
import pandas as pd
from datetime import datetime

# Portfolio holdings (when we bought stocks)
portfolio = pd.DataFrame({
 'Stock_ID': [1, 5, 10, 9, 7],
 'Stock_Symbol': ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN'],
 'Purchase_Date': ['2023-03-15', '2023-07-22', '2023-11-03', '2023-06-08', '2023-02-21'],
 'Shares': [100, 50, 25, 75, 30]
})

# Market price history (daily prices, but with gaps)
price_history = pd.DataFrame({
 'Stock_ID': [1, 1, 5, 5, 7, 7, 9, 9, 10, 10],
 'Price_Date': [
 '2023-03-14', '2023-03-17', # AAPL: missing 3/15, 3/16
 '2023-07-21', '2023-07-24', # MSFT: missing 7/22, 7/23 
 '2023-02-20', '2023-02-23', # AMZN: missing 2/21, 2/22
 '2023-06-07', '2023-06-09', # TSLA: missing 6/8
 '2023-11-02', '2023-11-06' # GOOGL: missing 11/3, 11/4, 11/5
 ],
 'Price': [145.50, 147.20, 335.80, 338.90, 94.75, 96.30, 245.60, 248.10, 2750.00, 2780.50]
})

print("Portfolio Holdings:")
print(portfolio)
print("\nPrice History (with gaps):")
print(price_history)
print()

# Step 1: Convert date columns to datetime
portfolio['Purchase_Date'] = pd.to_datetime(portfolio['Purchase_Date'])
price_history['Price_Date'] = pd.to_datetime(price_history['Price_Date'])

# Step 2: Sort both dataframes (required for merge_asof)
portfolio = portfolio.sort_values(['Stock_ID', 'Purchase_Date'])
price_history = price_history.sort_values(['Stock_ID', 'Price_Date'])

print("Data sorted by Stock_ID and dates:")
print("Portfolio sorted:")
print(portfolio)
print("\nPrice history sorted:")
print(price_history)
print()

# Step 3: Use merge_asof to find the most recent price for each purchase
# This finds the latest price that was available on or before the purchase date
valued_portfolio = pd.merge_asof(
 portfolio, # Left dataframe (what we want to value)
 price_history, # Right dataframe (price history)
 left_on='Purchase_Date', # Date column in portfolio
 right_on='Price_Date', # Date column in prices
 by='Stock_ID', # Match within the same stock
 direction='backward' # Find most recent price before/on purchase date
)

print("Portfolio with matched prices:")
print(valued_portfolio)
print()

# Step 4: Calculate portfolio value
valued_portfolio['Position_Value'] = valued_portfolio['Shares'] * valued_portfolio['Price']
valued_portfolio['Days_Between'] = (valued_portfolio['Purchase_Date'] - valued_portfolio['Price_Date']).dt.days

print("Final Portfolio Valuation:")
print(valued_portfolio[['Stock_Symbol', 'Purchase_Date', 'Price_Date', 'Days_Between', 'Shares', 'Price', 'Position_Value']])
print()

# Step 5: Show the matching logic in detail
print("Detailed Matching Analysis:")
for _, row in valued_portfolio.iterrows():
 print(f"{row['Stock_Symbol']}: Purchased on {row['Purchase_Date'].strftime('%Y-%m-%d')}, "
 f"valued using price from {row['Price_Date'].strftime('%Y-%m-%d')} "
 f"({row['Days_Between']} days earlier) at ${row['Price']:.2f}")
print()

# Step 6: Portfolio summary
total_value = valued_portfolio['Position_Value'].sum()
avg_price_lag = valued_portfolio['Days_Between'].mean()

summary = pd.DataFrame({
 'Metric': [
 'Total Positions',
 'Total Portfolio Value',
 'Average Price Lag (days)',
 'Largest Position Value',
 'Positions with Same-Day Pricing'
 ],
 'Value': [
 len(valued_portfolio),
 f"${total_value:,.2f}",
 f"{avg_price_lag:.1f}",
 f"${valued_portfolio['Position_Value'].max():,.2f}",
 (valued_portfolio['Days_Between'] == 0).sum()
 ]
})

print("Portfolio Valuation Summary:")
print(summary.to_string(index=False))
print()

# Step 7: Demonstrate different merge_asof directions
print("Comparison of different merge directions:")

# Backward search (most recent price before purchase)
backward_merge = pd.merge_asof(
 portfolio, price_history,
 left_on='Purchase_Date', right_on='Price_Date',
 by='Stock_ID', direction='backward'
)

# Forward search (earliest price after purchase) 
forward_merge = pd.merge_asof(
 portfolio, price_history,
 left_on='Purchase_Date', right_on='Price_Date', 
 by='Stock_ID', direction='forward'
)

# Nearest search (closest price in either direction)
nearest_merge = pd.merge_asof(
 portfolio, price_history,
 left_on='Purchase_Date', right_on='Price_Date',
 by='Stock_ID', direction='nearest'
)

comparison = pd.DataFrame({
 'Stock': portfolio['Stock_Symbol'],
 'Purchase_Date': portfolio['Purchase_Date'],
 'Backward_Price': backward_merge['Price'],
 'Forward_Price': forward_merge['Price'], 
 'Nearest_Price': nearest_merge['Price']
})

print("Different merge_asof directions:")
print(comparison)
```

## Key Learning Points

- **merge_asof handles imperfect data**: When exact matches aren't available, it finds the closest available information
- **Direction matters**: 'backward' finds the most recent past value, 'forward' finds the next future value, 'nearest' finds the closest in either direction
- **Perfect for financial data**: Stock prices, exchange rates, interest rates often have gaps but you need the most recent available rate
- **Sorting is critical**: Both datasets must be sorted by the merge keys and date columns for merge_asof to work correctly
- **Handles one-to-many relationships**: Multiple price points can exist for each stock, and merge_asof picks the appropriate one
- **Real-world data is messy**: Markets are closed on weekends, data feeds have gaps, but business logic still needs the "nearest available" information

---

*Ready for your next mystery? Check out the [Masha & Panda Mystery Series](/mysteries) for more accounting adventures!*