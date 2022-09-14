Suppose we have a table in excel with some random amounts and suppose you'd want to divide these
amounts by let's say 100 but you want the result to appear as a "hardcoded" value instead of a formula
It would be time consuming and extremely inefficient to have to type each of the values.  What's a better
apprach?

Below is a smaple Data Frame with some random generated values

```df_original =pd.DataFrame( np.random.default_rng().uniform(low=10000,high=1000000,size=[2,10]))```

![Original dataframe](C:\Users\nplatchk\Desktop\df_original)

let's divide each of the values by 100 and then round the result to the nearest integer

```df=(df_original.values/100).round().astype(int)```

![Resulting dataframe](C:\Users\nplatchk\Desktop\df)

Now copy and paste, no formulas!
