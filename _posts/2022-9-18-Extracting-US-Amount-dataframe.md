---
layout: post
title: Amount in US dollars/cents extracted from a string
subtitle: US dollar amount extracted into a separate column of a dataframe
tags: [pandas, US dollars, regex,dataframe,extract]
---
![](https://imgur.com/2yhAks8)




Extract an amount (US dollars dominated) into a separate column of a dataframe using regex


```python
import pandas as pd
```


```python
import re
```


```python
df=pd.DataFrame({"Description":['A','B','C','D','E'],"Amount":['trx .11','balance 536,002.63','adj 85.85','manual adj 0.00','fx va vb 55.63']})
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
      <th>Description</th>
      <th>Amount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>trx .11</td>
    </tr>
    <tr>
      <th>1</th>
      <td>B</td>
      <td>balance 536,002.63</td>
    </tr>
    <tr>
      <th>2</th>
      <td>C</td>
      <td>adj 85.85</td>
    </tr>
    <tr>
      <th>3</th>
      <td>D</td>
      <td>manual adj 0.00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>E</td>
      <td>fx va vb 55.63</td>
    </tr>
  </tbody>
</table>
</div>




```python
match='(\$?(?<!\d)(?:\d{1,3}(?:,\d{3})*|\d{4,})?\.?\d+)'
```


```python
df['Amount_extract']=df['Amount'].str.extract(match)
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
      <th>Description</th>
      <th>Amount</th>
      <th>Amount_extract</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>trx .11</td>
      <td>.11</td>
    </tr>
    <tr>
      <th>1</th>
      <td>B</td>
      <td>balance 536,002.63</td>
      <td>536,002.63</td>
    </tr>
    <tr>
      <th>2</th>
      <td>C</td>
      <td>adj 85.85</td>
      <td>85.85</td>
    </tr>
    <tr>
      <th>3</th>
      <td>D</td>
      <td>manual adj 0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>E</td>
      <td>fx va vb 55.63</td>
      <td>55.63</td>
    </tr>
  </tbody>
</table>
</div>


