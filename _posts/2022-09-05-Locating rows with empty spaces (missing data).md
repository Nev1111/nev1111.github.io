# Locate rows with empty spaces (nan)

Here's a quick way to clean up a table that has empty spaces (aka nans)

`df_nan=df[df.isna().any(axis=1)]`
