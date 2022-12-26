Removing rows with empty values (nan)
Here's a quick way to clean up a table by removing rows with empty values (nan).

`df_nan=df[df.isna().any(axis=1)]`
