{
  "metadata": {
    "language_info": {
      "codemirror_mode": {
        "name": "python",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.8"
    },
    "kernelspec": {
      "name": "python",
      "display_name": "Python (Pyodide)",
      "language": "python"
    }
  },
  "nbformat_minor": 4,
  "nbformat": 4,
  "cells": [
    {
      "cell_type": "code",
      "source": "import pandas as pd ",
      "metadata": {},
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": "#Convert old legacy system balances ending with '-' to negative values, if there's an annoying \"-\" negative sign at the end of the number",
      "metadata": {
        "trusted": true
      },
      "execution_count": 1,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": "df.loc[mask, 'Amount'] = '-' + df.loc[mask, 'Amount'].str[:-1] ",
      "metadata": {}
    },
    {
      "cell_type": "markdown",
      "source": " mask = df['Amount'].str.endswith('-')",
      "metadata": {}
    },
    {
      "cell_type": "markdown",
      "source": "df['Amount']=df['Amount'].str.replace(',','')",
      "metadata": {}
    },
    {
      "cell_type": "markdown",
      "source": "df['Amount']=df['Amount'].astype(float)",
      "metadata": {}
    }
  ]
}