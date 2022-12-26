---
layout: post
title: Amount in US dollars/cents extracted from a string
subtitle: A method for extracting US dollar amounts into a separate column of a dataframe.
thumbnail-img: /assets/img/PandAudit background transparent.png
tags: [pandas, US dollars, regex,dataframe,extract]
---


If you have an unstructured file with messy strings containing amounts, and you want to extract just the amounts, you might consider the following approach:

First, you will need to identify the patterns in the strings that indicate the presence of an amount. For example, you might look for strings that contain a currency symbol, such as "$" or "€", or strings that contain numbers followed by a unit of measurement, such as "kg" or "lbs".

Once you have identified the patterns that indicate the presence of an amount, you can use regular expressions or string manipulation techniques to extract the amounts from the strings. This may involve using functions such as re.search or re.findall in Python, or using string functions such as split or replace to extract the amounts.

After extracting the amounts, you may want to convert them to a numeric data type, such as float or integer, in order to perform calculations with them. You can do this using functions such as int() or float(), depending on the data type you desire.

Finally, you can store the extracted and converted amounts in a new column in your DataFrame, or use them for further analysis or processing as needed.

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


