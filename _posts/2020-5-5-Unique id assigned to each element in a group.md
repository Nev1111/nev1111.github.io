---
layout: post
title: Assign unique ID to a group in a dataframe
subtitle: Assign an id that is unique to each element in a group
thumbnail-img: /assets/img/PandAudit background transparent.png
tags: [pandas, Excel, unique, unique ID, group, dataframe]
---
The purpose of this code is to group the elements in the 'A' column of a Pandas DataFrame and assign a sequential ID to each group. The ID is assigned starting with one and increasing by one for each group.

To do this, the code first imports the pandas library and creates a DataFrame dataset with a single column 'A' containing a series of values.

Then, it adds a new column called 'group_ID' to the DataFrame by using the groupby() method to group the elements in the 'A' column, and the ngroup() method to assign a group number to each element. The group numbers start at zero, so the code adds one to each group number to get the desired sequential IDs starting with one.

Finally, the code displays the resulting DataFrame with the group_ID column added.

This code would be useful for grouping common elements in a DataFrame and assigning a sequential ID to each group, which could be useful for further analysis or visualization of the data.



```python
import pandas as pd
```


```python
dataset=pd.DataFrame({'A': [1, 1, 1,2,2,2,1,3,2,3,3]})
print(dataset)
```

        A
    0   1
    1   1
    2   1
    3   2
    4   2
    5   2
    6   1
    7   3
    8   2
    9   3
    10  3
    


```python
dataset['id']=dataset.groupby('A').cumcount()
print(dataset)
```

        A  id
    0   1   0
    1   1   1
    2   1   2
    3   2   0
    4   2   1
    5   2   2
    6   1   3
    7   3   0
    8   2   3
    9   3   1
    10  3   2
    

Note that the values contained in column 'A' do not need to be sorted prior to applying this function.
