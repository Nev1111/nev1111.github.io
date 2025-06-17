---
layout: page
title: Excel to Pandas Cheatsheet
permalink: /cheatsheet/
---

# 📊 Excel to Pandas Cheatsheet

| Excel Function        | Pandas Equivalent                     |
|-----------------------|----------------------------------------|
| `VLOOKUP()`           | `merge()`                              |
| Pivot Table           | `pivot_table()`                        |
| Filter                | `df[df["col"] == "value"]`             |
| SUMIFS                | `groupby()` + `sum()`                  |
| Remove Duplicates     | `drop_duplicates()`                    |
| Sort                  | `sort_values(by="col")`                |
| IF Formula            | `np.where()` or `df.apply()`           |
