---
layout: post
title: The as of merge - python [pandas]
subtitle: Merging datasets on the nearest or closest mathing value
thumbnail-img: /assets/img/PandAudit background transparent.png
tags: [pandas, as_of merge, regex,dataframe, merge_as_of,  pd.merge_asof()]
---

"Instead of using a "left" or "right" join, it is possible to merge two datasets based on the "nearest" or "closest" matching key values. This approach is known as a "merge on less than," "merge on greater than," or "merge on nearest elements" and is illustrated in the following example data sets:"



```python
#Create the sample dataframes 
import pandas as pd
data_set_A = pd.DataFrame({'key_column': [1, 5, 10,9,7], 'A_val_date': ['1/1/2015', '5/22/2019', '3/3/2020','6/8/2010','2/21/2009']})
data_set_B = pd.DataFrame({'key_column': [1,3,4,6,8,9], 'B_val_date': ['2/24/2013', '3/16/2014','1/09/2009','2/27/2016','5/1/2014','3/9/2012']})

#convert the values in 'A_val' and 'B_val' to datetime objects
data_set_A['A_val_date']=pd.to_datetime(data_set_A['A_val_date'])
data_set_B['B_val_date']=pd.to_datetime(data_set_B['B_val_date'])

#display the dataframes
print (data_set_A)
print (data_set_B)

```

       key_column A_val_date
    0           1 2015-01-01
    1           5 2019-05-22
    2          10 2020-03-03
    3           9 2010-06-08
    4           7 2009-02-21
       key_column B_val_date
    0           1 2013-02-24
    1           3 2014-03-16
    2           4 2009-01-09
    3           6 2016-02-27
    4           8 2014-05-01
    5           9 2012-03-09
    

The objective of this merge operation is to combine the values from data_set_A with those from data_set_B, using the shared column 'key_column' as the reference. The resulting dataset should include all rows from data_set_A and only those rows from data_set_B that match the values in data_set_A. If there is no exact match, the merge should use the last row in data_set_B whose 'key_column' value is less than the 'key_column' value in data_set_A, which is known as a "backward" search.


```python
# First, sort the values contained in 'A_val' and 'B_val' by ascending order
data_set_A=data_set_A.sort_values(by='key_column')
data_set_B=data_set_B.sort_values(by='key_column')
```


```python
resulting_data_set=pd.merge_asof(data_set_A,data_set_B,on='key_column')
print(resulting_data_set)
```

       key_column A_val_date B_val_date
    0           1 2015-01-01 2013-02-24
    1           5 2019-05-22 2009-01-09
    2           7 2009-02-21 2016-02-27
    3           9 2010-06-08 2012-03-09
    4          10 2020-03-03 2012-03-09
    

In the given scenario, the first row in data_set_A has an exact match in data_set_B for the 'key_column' value of '1', so the dates 2015-01-01 and 2013-01-24 are paired. However, the second row in data_set_A has a 'key_column' value of '5' which does not have a matching value in data_set_B. In this case, the closest value in data_set_B with a 'key_column' value less than '5' is the row with a 'key_column' value of '4' and a corresponding date value of 2009-01-09.

This type of merge can also be performed in the opposite direction, where the first row in data_set_B is selected whose 'key_column' value is greater than or equal to the value in the 'key_column' of data_set_A. By default, this type of search is performed in the "backward" direction, but the 'direction' parameter can be set to 'forward' to specify that the search should be performed in the opposite direction.


```python
resulting_data_set=pd.merge_asof(data_set_A,data_set_B,on='key_column',direction='forward')
print(resulting_data_set)
```

       key_column A_val_date B_val_date
    0           1 2015-01-01 2013-02-24
    1           5 2019-05-22 2016-02-27
    2           7 2009-02-21 2014-05-01
    3           9 2010-06-08 2012-03-09
    4          10 2020-03-03        NaT
    

Note: the last row has a 'NaT' mathing value, because the value '10' in the 'key_column' contained in data_set_A does not have an equal or a greater corresponding 'key_column' value in 'data_set_B'. 

To perform a merge on a 'nearest' basis, the 'direction' paramenter needs to be set to 'nearest'.  See results below:


```python
resulting_data_set=pd.merge_asof(data_set_A,data_set_B,on='key_column',direction='nearest')
print(resulting_data_set)
```

       key_column A_val_date B_val_date
    0           1 2015-01-01 2013-02-24
    1           5 2019-05-22 2009-01-09
    2           7 2009-02-21 2016-02-27
    3           9 2010-06-08 2012-03-09
    4          10 2020-03-03 2012-03-09
    

This method is also explained in Pandas' documentation
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.merge_asof.html
