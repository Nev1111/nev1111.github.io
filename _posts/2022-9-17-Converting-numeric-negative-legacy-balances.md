---
layout: post
title: Formatting legacy system negative balances
thumbnail-img: /assets/img/PandAudit background transparent.png
subtitle: Convert old legacy system balances ending with '-' OR 'CR' to negative values
tags: [pandas, Excel, totals, formulas, hardcoded]
---

This post is about formatting negative balances in a legacy system so that they can be easily processed in a modern system. The post provides a method using the pandas library in Python to convert old legacy system balances, which may be formatted with a '-' or 'CR' suffix, to negative values. The method involves reading the legacy system values into a pandas dataframe, creating a mask to identify rows with negative balances, and then using the mask to replace the '-' or 'CR' suffix with a negative symbol. The resulting values are then formatted by removing any commas and converting them to float data type. The final dataframe contains the correctly formatted negative values.

Here is a method for converting a figure from an old, legacy file, such as "5,009-".


```python
import pandas as pd
```


```python
df=pd.DataFrame({'Amount':['5,009-', '69.35-', '8,959-','8,953.23','10,520']})
```


```python
df
```




<div>
<style scoped>
 .dataframe tbody tr th:only-of-type {
 vertical-align: middle;
 }

 .dataframe tbody tr th {
 vertical-align: top;
 }

 .dataframe thead th {
 text-align: right;
 }
</style>
<table border="1" class="dataframe">
 <thead>
 <tr style="text-align: right;">
 <th></th>
 <th>Amount</th>
 </tr>
 </thead>
 <tbody>
 <tr>
 <th>0</th>
 <td>5,009-</td>
 </tr>
 <tr>
 <th>1</th>
 <td>69.35-</td>
 </tr>
 <tr>
 <th>2</th>
 <td>8,959-</td>
 </tr>
 <tr>
 <th>3</th>
 <td>8,953.23</td>
 </tr>
 <tr>
 <th>4</th>
 <td>10,520</td>
 </tr>
 </tbody>
</table>
</div>




```python
mask = df['Amount'].str.endswith('-')
```


```python
df.loc[mask, 'Amount'] = '-' + df.loc[mask, 'Amount'].str[:-1]
```


```python
df['Amount']=df['Amount'].str.replace(',','')
```


```python
df['Amount']=df['Amount'].astype(float)
```


```python
df
```




<div>
<style scoped>
 .dataframe tbody tr th:only-of-type {
 vertical-align: middle;
 }

 .dataframe tbody tr th {
 vertical-align: top;
 }

 .dataframe thead th {
 text-align: right;
 }
</style>
<table border="1" class="dataframe">
 <thead>
 <tr style="text-align: right;">
 <th></th>
 <th>Amount</th>
 </tr>
 </thead>
 <tbody>
 <tr>
 <th>0</th>
 <td>-5009.00</td>
 </tr>
 <tr>
 <th>1</th>
 <td>-69.35</td>
 </tr>
 <tr>
 <th>2</th>
 <td>-8959.00</td>
 </tr>
 <tr>
 <th>3</th>
 <td>8953.23</td>
 </tr>
 <tr>
 <th>4</th>
 <td>10520.00</td>
 </tr>
 </tbody>
</table>
</div>




```python

```
