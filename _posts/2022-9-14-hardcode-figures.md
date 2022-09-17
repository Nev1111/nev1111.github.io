---
layout: post
title: Getting rid of formulas/Hardcoding figures in Excel
subtitle: Making sure totals are exact amounts
tags: [pandas, Excel, totals, formulas, hardcoded]
---

Suppose we have a table in excel with some random amounts and we want to do something with these amounts (ex: divide by 100). This is easily accomplished through Excel by just typing in "=amount/100" but in the world of financial reporting and investment accounting, 
it is often the case when formulas cause discrepancies in total values (they're off by some amount).  This is especially true if decimals are involved. It would be time consuming and extremely inefficient to have to type each of the values in the cells one by one.  So what's a better approach?

Below is a sample Data Frame with some random generated values

```df_original =pd.DataFrame( np.random.default_rng().uniform(low=10000,high=1000000,size=[2,10]))```

![Original dataframe](C:\Users\nplatchk\Desktop\df_original)

let's divide each of the values by 100 and then round the result to the nearest integer

```df=(df_original.values/100).round().astype(int)```

![Resulting dataframe](C:\Users\nplatchk\Desktop\df)

Now copy and paste, no formulas!
