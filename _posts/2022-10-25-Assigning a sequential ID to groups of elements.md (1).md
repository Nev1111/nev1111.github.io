---
layout: post
title: Assign an ID to common elements of a dataframe
subtitle: Group elements together and assign an ID to each of the groups
thumbnail-img: /assets/img/PandAudit background transparent.png
tags: [pandas, groupby, sequential ID, dataframe, common elements]
---



This post will demonstrate how to group elements in a DataFrame and assign a sequential ID to each group, starting with one and increasing by one for each group.

So here is a sample DataFrame:


```python
import pandas as pd
dataset=pd.DataFrame({'A': ['A', 'A', 'A','B','B','B','A','C','B','C','C']})
```


```python
dataset
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
      <th>A</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A</td>
    </tr>
    <tr>
      <th>3</th>
      <td>B</td>
    </tr>
    <tr>
      <th>4</th>
      <td>B</td>
    </tr>
    <tr>
      <th>5</th>
      <td>B</td>
    </tr>
    <tr>
      <th>6</th>
      <td>A</td>
    </tr>
    <tr>
      <th>7</th>
      <td>C</td>
    </tr>
    <tr>
      <th>8</th>
      <td>B</td>
    </tr>
    <tr>
      <th>9</th>
      <td>C</td>
    </tr>
    <tr>
      <th>10</th>
      <td>C</td>
    </tr>
  </tbody>
</table>
</div>




```python
dataset['group_ID']=dataset.groupby('A').ngroup()+1
```


```python
dataset
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
      <th>A</th>
      <th>group_ID</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>B</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>B</td>
      <td>2</td>
    </tr>
    <tr>
      <th>5</th>
      <td>B</td>
      <td>2</td>
    </tr>
    <tr>
      <th>6</th>
      <td>A</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>C</td>
      <td>3</td>
    </tr>
    <tr>
      <th>8</th>
      <td>B</td>
      <td>2</td>
    </tr>
    <tr>
      <th>9</th>
      <td>C</td>
      <td>3</td>
    </tr>
    <tr>
      <th>10</th>
      <td>C</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>



Notice how the elements in 'A' do not need to be pre-sorted before assigning the group_ID
