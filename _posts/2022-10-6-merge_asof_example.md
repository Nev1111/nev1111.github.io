---
layout: post
title: Merge/Join tables on the closest date in time
subtitle: Merge_asof pandas example
thumbnail-img: /assets/img/PandAudit background transparent.png
tags: [pandas, merge, merge_asof, dataframe, closest match]
---

In this post, we demonstrate how to use the merge_asof() function in the Pandas library to merge two dataframes, df1 and df2, where df1 contains names and IDs for certain individuals and df2 contains historical addresses for those same individuals. The goal is to match each person in df1 with a corresponding address in df2 that is closest to a specified cutoff date.

The cutoff date can be any date, such as today or last year, and is used to determine which address from the historical data in df2 is the most relevant to use in the merge. For example, if the cutoff date is January 1, 2022, and an individual has three historical addresses, the address that is closest in time (and not exceeding) the cutoff date will be used in the merge.

To begin, the code imports the Pandas library and creates two dataframes: df1, which contains names and IDs for individuals, and df2, which contains historical addresses for those same individuals.

Next, the code converts the 'Effective Date' column in df2 to a datetime format using the to_datetime() function.

Then, the code sorts the rows of df2 by the 'Effective Date' column in ascending order using the sort_values() function. This is important because the merge_asof() function expects the data to be sorted in order to properly match rows based on the cutoff date.

Finally, the code uses the merge_asof() function to merge df1 and df2 based on the 'ID' column and the cutoff date. The merge_asof() function returns a new dataframe that includes the matching rows from both df1 and df2, along with any additional columns that are specified in the function.

Overall, this code demonstrates how to use the merge_asof() function in Pandas to merge two dataframes based on the closest date in time. [Further explained below]



```python
import pandas as pd
```




```python
df1
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
 <th>Name</th>
 <th>ID</th>
 </tr>
 </thead>
 <tbody>
 <tr>
 <th>0</th>
 <td>Jane Smith</td>
 <td>2</td>
 </tr>
 <tr>
 <th>1</th>
 <td>John Doe</td>
 <td>1</td>
 </tr>
 <tr>
 <th>2</th>
 <td>Johnathan Adams</td>
 <td>5</td>
 </tr>
 <tr>
 <th>3</th>
 <td>Kimberly Smith</td>
 <td>8</td>
 </tr>
 <tr>
 <th>4</th>
 <td>Mary Brown</td>
 <td>4</td>
 </tr>
 <tr>
 <th>5</th>
 <td>Mike Jones</td>
 <td>3</td>
 </tr>
 <tr>
 <th>6</th>
 <td>Sara Davis</td>
 <td>6</td>
 </tr>
 <tr>
 <th>7</th>
 <td>Will Johnson</td>
 <td>7</td>
 </tr>
 </tbody>
</table>
</div>







```python
df2
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
 <th>ID</th>
 <th>Name</th>
 <th>Address 1</th>
 <th>Address 2</th>
 <th>City</th>
 <th>State</th>
 <th>Country</th>
 <th>Zip</th>
 <th>Effective Date</th>
 </tr>
 </thead>
 <tbody>
 <tr>
 <th>0</th>
 <td>1</td>
 <td>John Doe</td>
 <td>123 Main St</td>
 <td>Suite 100</td>
 <td>San Francisco</td>
 <td>CA</td>
 <td>USA</td>
 <td>94105</td>
 <td>2016-05-02</td>
 </tr>
 <tr>
 <th>1</th>
 <td>1</td>
 <td>John Doe</td>
 <td>222 Post St,</td>
 <td>NaN</td>
 <td>San Francisco</td>
 <td>CA</td>
 <td>USA</td>
 <td>94108</td>
 <td>2018-01-01</td>
 </tr>
 <tr>
 <th>2</th>
 <td>1</td>
 <td>John Doe</td>
 <td>456 Market St,</td>
 <td>NaN</td>
 <td>San Francisco</td>
 <td>CA</td>
 <td>USA</td>
 <td>94103</td>
 <td>2021-03-22</td>
 </tr>
 <tr>
 <th>3</th>
 <td>2</td>
 <td>Jane Smith</td>
 <td>456 Elm St</td>
 <td>Apt 4</td>
 <td>New York</td>
 <td>NY</td>
 <td>USA</td>
 <td>10012</td>
 <td>2021-09-05</td>
 </tr>
 <tr>
 <th>4</th>
 <td>2</td>
 <td>Jane Smith</td>
 <td>620 Reiss Pl</td>
 <td>Apt 2D</td>
 <td>Bronx</td>
 <td>NY</td>
 <td>USA</td>
 <td>12345</td>
 <td>2001-10-23</td>
 </tr>
 <tr>
 <th>5</th>
 <td>2</td>
 <td>Jane Smith</td>
 <td>3484 Fort Independence St</td>
 <td>NaN</td>
 <td>Glen Oaks</td>
 <td>NY</td>
 <td>USA</td>
 <td>11004</td>
 <td>2008-11-15</td>
 </tr>
 <tr>
 <th>6</th>
 <td>3</td>
 <td>Mike Jones</td>
 <td>789 Pine St</td>
 <td>Floor 2</td>
 <td>Seattle</td>
 <td>WA</td>
 <td>USA</td>
 <td>98101</td>
 <td>2015-10-09</td>
 </tr>
 <tr>
 <th>7</th>
 <td>3</td>
 <td>Mike Jones</td>
 <td>26142A Langston Ave</td>
 <td>NaN</td>
 <td>New York</td>
 <td>NY</td>
 <td>USA</td>
 <td>59712</td>
 <td>2020-01-28</td>
 </tr>
 <tr>
 <th>8</th>
 <td>3</td>
 <td>Mike Jones</td>
 <td>620 Reiss Pl</td>
 <td>NaN</td>
 <td>Staten Island</td>
 <td>NY</td>
 <td>USA</td>
 <td>56712</td>
 <td>2020-02-09</td>
 </tr>
 <tr>
 <th>9</th>
 <td>3</td>
 <td>Mike Jones</td>
 <td>379 Amboy St</td>
 <td>NaN</td>
 <td>Rockville Centre</td>
 <td>NY</td>
 <td>USA</td>
 <td>56921</td>
 <td>2020-01-24</td>
 </tr>
 <tr>
 <th>10</th>
 <td>4</td>
 <td>Mary Brown</td>
 <td>111 1st Ave</td>
 <td>Apt 5</td>
 <td>Los Angeles</td>
 <td>CA</td>
 <td>USA</td>
 <td>90012</td>
 <td>2019-08-06</td>
 </tr>
 <tr>
 <th>11</th>
 <td>4</td>
 <td>Mary Brown</td>
 <td>5530 99th St</td>
 <td>NaN</td>
 <td>White Plains</td>
 <td>NY</td>
 <td>USA</td>
 <td>15637</td>
 <td>2019-01-23</td>
 </tr>
 <tr>
 <th>12</th>
 <td>5</td>
 <td>Johnathan Adams</td>
 <td>222 2nd St</td>
 <td>Ste 200</td>
 <td>Chicago</td>
 <td>IL</td>
 <td>USA</td>
 <td>60606</td>
 <td>2015-06-07</td>
 </tr>
 <tr>
 <th>13</th>
 <td>5</td>
 <td>Johnathan Adams</td>
 <td>477 De Mott Ave</td>
 <td>NaN</td>
 <td>New Hyde Park</td>
 <td>NY</td>
 <td>USA</td>
 <td>10023</td>
 <td>2019-01-13</td>
 </tr>
 <tr>
 <th>14</th>
 <td>6</td>
 <td>Sara Davis</td>
 <td>333 3rd Ave</td>
 <td>Floor 4</td>
 <td>Houston</td>
 <td>TX</td>
 <td>USA</td>
 <td>77001</td>
 <td>2020-08-03</td>
 </tr>
 <tr>
 <th>15</th>
 <td>6</td>
 <td>Sara Davis</td>
 <td>76 Shotwell Ave</td>
 <td>NaN</td>
 <td>Bronx</td>
 <td>NY</td>
 <td>USA</td>
 <td>15893</td>
 <td>2019-01-05</td>
 </tr>
 <tr>
 <th>16</th>
 <td>7</td>
 <td>Will Johnson</td>
 <td>444 4th St</td>
 <td>Apt 6</td>
 <td>Philadelphia</td>
 <td>PA</td>
 <td>USA</td>
 <td>19106</td>
 <td>2015-05-09</td>
 </tr>
 <tr>
 <th>17</th>
 <td>8</td>
 <td>Kimberly Smith</td>
 <td>555 5th Ave</td>
 <td>Apt 7</td>
 <td>Phoenix</td>
 <td>AZ</td>
 <td>USA</td>
 <td>85001</td>
 <td>2017-12-06</td>
 </tr>
 </tbody>
</table>
</div>



So for presentation purposes, let's say the cutoff date is 1/1/2022. Notice John Doe (ID1) has three historical addresses. The one where he resided that is closest in time (and not to exceed) the cutoff date is the "456 Market St" address with and effective date of "2021-03-22". 

First, we ensure that the "Effective Date" column is in a datetime format.


```python
df2['Effective Date']=pd.to_datetime(df2['Effective Date'])
```

Next, we need to sort by the Effective Date in an ascending order.


```python
df2.sort_values(by='Effective Date',inplace=True)
```


```python
df2
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
 <th>ID</th>
 <th>Name</th>
 <th>Address 1</th>
 <th>Address 2</th>
 <th>City</th>
 <th>State</th>
 <th>Country</th>
 <th>Zip</th>
 <th>Effective Date</th>
 </tr>
 </thead>
 <tbody>
 <tr>
 <th>4</th>
 <td>2</td>
 <td>Jane Smith</td>
 <td>620 Reiss Pl</td>
 <td>Apt 2D</td>
 <td>Bronx</td>
 <td>NY</td>
 <td>USA</td>
 <td>12345</td>
 <td>2001-10-23</td>
 </tr>
 <tr>
 <th>5</th>
 <td>2</td>
 <td>Jane Smith</td>
 <td>3484 Fort Independence St</td>
 <td>NaN</td>
 <td>Glen Oaks</td>
 <td>NY</td>
 <td>USA</td>
 <td>11004</td>
 <td>2008-11-15</td>
 </tr>
 <tr>
 <th>16</th>
 <td>7</td>
 <td>Will Johnson</td>
 <td>444 4th St</td>
 <td>Apt 6</td>
 <td>Philadelphia</td>
 <td>PA</td>
 <td>USA</td>
 <td>19106</td>
 <td>2015-05-09</td>
 </tr>
 <tr>
 <th>12</th>
 <td>5</td>
 <td>Johnathan Adams</td>
 <td>222 2nd St</td>
 <td>Ste 200</td>
 <td>Chicago</td>
 <td>IL</td>
 <td>USA</td>
 <td>60606</td>
 <td>2015-06-07</td>
 </tr>
 <tr>
 <th>6</th>
 <td>3</td>
 <td>Mike Jones</td>
 <td>789 Pine St</td>
 <td>Floor 2</td>
 <td>Seattle</td>
 <td>WA</td>
 <td>USA</td>
 <td>98101</td>
 <td>2015-10-09</td>
 </tr>
 <tr>
 <th>0</th>
 <td>1</td>
 <td>John Doe</td>
 <td>123 Main St</td>
 <td>Suite 100</td>
 <td>San Francisco</td>
 <td>CA</td>
 <td>USA</td>
 <td>94105</td>
 <td>2016-05-02</td>
 </tr>
 <tr>
 <th>17</th>
 <td>8</td>
 <td>Kimberly Smith</td>
 <td>555 5th Ave</td>
 <td>Apt 7</td>
 <td>Phoenix</td>
 <td>AZ</td>
 <td>USA</td>
 <td>85001</td>
 <td>2017-12-06</td>
 </tr>
 <tr>
 <th>1</th>
 <td>1</td>
 <td>John Doe</td>
 <td>222 Post St,</td>
 <td>NaN</td>
 <td>San Francisco</td>
 <td>CA</td>
 <td>USA</td>
 <td>94108</td>
 <td>2018-01-01</td>
 </tr>
 <tr>
 <th>15</th>
 <td>6</td>
 <td>Sara Davis</td>
 <td>76 Shotwell Ave</td>
 <td>NaN</td>
 <td>Bronx</td>
 <td>NY</td>
 <td>USA</td>
 <td>15893</td>
 <td>2019-01-05</td>
 </tr>
 <tr>
 <th>13</th>
 <td>5</td>
 <td>Johnathan Adams</td>
 <td>477 De Mott Ave</td>
 <td>NaN</td>
 <td>New Hyde Park</td>
 <td>NY</td>
 <td>USA</td>
 <td>10023</td>
 <td>2019-01-13</td>
 </tr>
 <tr>
 <th>11</th>
 <td>4</td>
 <td>Mary Brown</td>
 <td>5530 99th St</td>
 <td>NaN</td>
 <td>White Plains</td>
 <td>NY</td>
 <td>USA</td>
 <td>15637</td>
 <td>2019-01-23</td>
 </tr>
 <tr>
 <th>10</th>
 <td>4</td>
 <td>Mary Brown</td>
 <td>111 1st Ave</td>
 <td>Apt 5</td>
 <td>Los Angeles</td>
 <td>CA</td>
 <td>USA</td>
 <td>90012</td>
 <td>2019-08-06</td>
 </tr>
 <tr>
 <th>9</th>
 <td>3</td>
 <td>Mike Jones</td>
 <td>379 Amboy St</td>
 <td>NaN</td>
 <td>Rockville Centre</td>
 <td>NY</td>
 <td>USA</td>
 <td>56921</td>
 <td>2020-01-24</td>
 </tr>
 <tr>
 <th>7</th>
 <td>3</td>
 <td>Mike Jones</td>
 <td>26142A Langston Ave</td>
 <td>NaN</td>
 <td>New York</td>
 <td>NY</td>
 <td>USA</td>
 <td>59712</td>
 <td>2020-01-28</td>
 </tr>
 <tr>
 <th>8</th>
 <td>3</td>
 <td>Mike Jones</td>
 <td>620 Reiss Pl</td>
 <td>NaN</td>
 <td>Staten Island</td>
 <td>NY</td>
 <td>USA</td>
 <td>56712</td>
 <td>2020-02-09</td>
 </tr>
 <tr>
 <th>14</th>
 <td>6</td>
 <td>Sara Davis</td>
 <td>333 3rd Ave</td>
 <td>Floor 4</td>
 <td>Houston</td>
 <td>TX</td>
 <td>USA</td>
 <td>77001</td>
 <td>2020-08-03</td>
 </tr>
 <tr>
 <th>2</th>
 <td>1</td>
 <td>John Doe</td>
 <td>456 Market St,</td>
 <td>NaN</td>
 <td>San Francisco</td>
 <td>CA</td>
 <td>USA</td>
 <td>94103</td>
 <td>2021-03-22</td>
 </tr>
 <tr>
 <th>3</th>
 <td>2</td>
 <td>Jane Smith</td>
 <td>456 Elm St</td>
 <td>Apt 4</td>
 <td>New York</td>
 <td>NY</td>
 <td>USA</td>
 <td>10012</td>
 <td>2021-09-05</td>
 </tr>
 </tbody>
</table>
</div>




```python

```

Also, we need to add the cutoff date to the first dataframe (df1) as a separate column (name it "Effective Date" to be consistent with df2


```python
df1['Effective Date']=pd.to_datetime('1/1/2022')
```


```python
df1.sort_values(by='Effective Date',inplace=True)
```


```python
df1
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
 <th>Name</th>
 <th>ID</th>
 <th>Effective Date</th>
 </tr>
 </thead>
 <tbody>
 <tr>
 <th>0</th>
 <td>Jane Smith</td>
 <td>2</td>
 <td>2022-01-01</td>
 </tr>
 <tr>
 <th>1</th>
 <td>John Doe</td>
 <td>1</td>
 <td>2022-01-01</td>
 </tr>
 <tr>
 <th>2</th>
 <td>Johnathan Adams</td>
 <td>5</td>
 <td>2022-01-01</td>
 </tr>
 <tr>
 <th>3</th>
 <td>Kimberly Smith</td>
 <td>8</td>
 <td>2022-01-01</td>
 </tr>
 <tr>
 <th>4</th>
 <td>Mary Brown</td>
 <td>4</td>
 <td>2022-01-01</td>
 </tr>
 <tr>
 <th>5</th>
 <td>Mike Jones</td>
 <td>3</td>
 <td>2022-01-01</td>
 </tr>
 <tr>
 <th>6</th>
 <td>Sara Davis</td>
 <td>6</td>
 <td>2022-01-01</td>
 </tr>
 <tr>
 <th>7</th>
 <td>Will Johnson</td>
 <td>7</td>
 <td>2022-01-01</td>
 </tr>
 </tbody>
</table>
</div>



 And now merge


```python
merged_df=pd.merge_asof(df1,df2, on = 'Effective Date', by='ID',direction='backward')
```


```python
merged_df
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
 <th>Name_x</th>
 <th>ID</th>
 <th>Effective Date</th>
 <th>Name_y</th>
 <th>Address 1</th>
 <th>Address 2</th>
 <th>City</th>
 <th>State</th>
 <th>Country</th>
 <th>Zip</th>
 </tr>
 </thead>
 <tbody>
 <tr>
 <th>0</th>
 <td>Jane Smith</td>
 <td>2</td>
 <td>2022-01-01</td>
 <td>Jane Smith</td>
 <td>456 Elm St</td>
 <td>Apt 4</td>
 <td>New York</td>
 <td>NY</td>
 <td>USA</td>
 <td>10012</td>
 </tr>
 <tr>
 <th>1</th>
 <td>John Doe</td>
 <td>1</td>
 <td>2022-01-01</td>
 <td>John Doe</td>
 <td>456 Market St,</td>
 <td>NaN</td>
 <td>San Francisco</td>
 <td>CA</td>
 <td>USA</td>
 <td>94103</td>
 </tr>
 <tr>
 <th>2</th>
 <td>Johnathan Adams</td>
 <td>5</td>
 <td>2022-01-01</td>
 <td>Johnathan Adams</td>
 <td>477 De Mott Ave</td>
 <td>NaN</td>
 <td>New Hyde Park</td>
 <td>NY</td>
 <td>USA</td>
 <td>10023</td>
 </tr>
 <tr>
 <th>3</th>
 <td>Kimberly Smith</td>
 <td>8</td>
 <td>2022-01-01</td>
 <td>Kimberly Smith</td>
 <td>555 5th Ave</td>
 <td>Apt 7</td>
 <td>Phoenix</td>
 <td>AZ</td>
 <td>USA</td>
 <td>85001</td>
 </tr>
 <tr>
 <th>4</th>
 <td>Mary Brown</td>
 <td>4</td>
 <td>2022-01-01</td>
 <td>Mary Brown</td>
 <td>111 1st Ave</td>
 <td>Apt 5</td>
 <td>Los Angeles</td>
 <td>CA</td>
 <td>USA</td>
 <td>90012</td>
 </tr>
 <tr>
 <th>5</th>
 <td>Mike Jones</td>
 <td>3</td>
 <td>2022-01-01</td>
 <td>Mike Jones</td>
 <td>620 Reiss Pl</td>
 <td>NaN</td>
 <td>Staten Island</td>
 <td>NY</td>
 <td>USA</td>
 <td>56712</td>
 </tr>
 <tr>
 <th>6</th>
 <td>Sara Davis</td>
 <td>6</td>
 <td>2022-01-01</td>
 <td>Sara Davis</td>
 <td>333 3rd Ave</td>
 <td>Floor 4</td>
 <td>Houston</td>
 <td>TX</td>
 <td>USA</td>
 <td>77001</td>
 </tr>
 <tr>
 <th>7</th>
 <td>Will Johnson</td>
 <td>7</td>
 <td>2022-01-01</td>
 <td>Will Johnson</td>
 <td>444 4th St</td>
 <td>Apt 6</td>
 <td>Philadelphia</td>
 <td>PA</td>
 <td>USA</td>
 <td>19106</td>
 </tr>
 </tbody>
</table>
</div>



And we get the expected results. Note: this merge can also be performed by finding the nearest match in the future, so the closest one past the cutoff date, and similarly on the nearest. This is accomplished by changing the direction parameter to forward or nearest. Additionally documentation on this function can be accessed via the link below.

[pandas.merge_asof](https://pandas.pydata.org/pandas-docs/dev/reference/api/pandas.merge_asof.html)

Also, to download anaconda along with its packages (python, and everything else you would need), go to this site, follow installation instructions:
[Download Anaconda link](https://anaconda.org/conda-forge/openai)

```python

```
