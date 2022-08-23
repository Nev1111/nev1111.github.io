import pandas as pd
#Convert old legacy system balances ending with '-' to negative values
mask = df['Amount'].str.endswith('-')
df.loc[mask, 'Amount'] = '-' + df.loc[mask, 'Amount'].str[:-1]
df['Amount']=df['Amount'].str.replace(',','')
df['Amount']=df['Amount'].astype(float)
