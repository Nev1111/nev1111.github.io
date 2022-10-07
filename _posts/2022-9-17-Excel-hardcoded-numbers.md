---
layout: post
title: Hardcoding figures in Excel
subtitle: Making sure totals are exact amounts/get rid of formulas in excel

tags: [pandas, Excel, totals, formulas, hardcoded]
---


```python
import pandas as pd
import numpy as np
```

Suppose we have a table in excel with some random amounts and we want to do something with these amounts (ex: divide by 100). This is easily accomplished through Excel by just typing in “=amount/100” but in the world of financial reporting and investment accounting, it is often the case when formulas cause discrepancies in total values (they’re off by some amount). This is especially true if decimals are involved. It would be time consuming and extremely inefficient to have to type each of the values in the cells one by one. So what’s a better approach?

Below is a sample Data Frame with some random generated values


```python
df_original =pd.DataFrame( np.random.default_rng().uniform(low=10000,high=1000000,size=[2,10]))
```


```python
df_original
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
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>191369.978330</td>
      <td>121242.362237</td>
      <td>485883.397567</td>
      <td>603730.730501</td>
      <td>540357.931392</td>
      <td>27475.613959</td>
      <td>547006.443044</td>
      <td>381619.857707</td>
      <td>719874.293255</td>
      <td>699297.825726</td>
    </tr>
    <tr>
      <th>1</th>
      <td>418524.493564</td>
      <td>761787.017200</td>
      <td>286310.298739</td>
      <td>598051.090853</td>
      <td>364419.574655</td>
      <td>64238.916384</td>
      <td>147163.925716</td>
      <td>631048.106704</td>
      <td>493904.806204</td>
      <td>195402.148564</td>
    </tr>
  </tbody>
</table>
</div>



let’s divide each of the values by 100 and then round the result to the nearest integer


```python
df=(df_original.values/100).round().astype(int)
```


```python
df
```




    array([[1914, 1212, 4859, 6037, 5404,  275, 5470, 3816, 7199, 6993],
           [4185, 7618, 2863, 5981, 3644,  642, 1472, 6310, 4939, 1954]])



Now copy and paste back into Excel, no formulas!
