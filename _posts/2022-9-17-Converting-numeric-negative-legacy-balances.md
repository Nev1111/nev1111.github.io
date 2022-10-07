---
layout: post
title: Formatting legacy system negative balances
thumbnail-img: /assets/img/PandAudit background transparent.png
subtitle: Convert old legacy system balances ending with '-' OR 'CR' to negative values
tags: [pandas, Excel, totals, formulas, hardcoded]
---

Here's a way to convert a figure from an old legacy file (ex. 5,009-)


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
