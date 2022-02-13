import itertools
import pandas as pd


def year_month_day_iter(years: list, months: list, days: list):
    return itertools.product(*[years, months, days])


def period_year_iter(start_year: int, end_year: int, period: int):
    ret = []
    for i in range(start_year, end_year+1):
        ret.append(list(range(i, i+period)))
    return ret


def year_date_df(data, iters):
    df_plot = pd.DataFrame(columns=["start_year", "date", "earns"])
    for i, (year, day) in enumerate(iters):
        df_plot = df_plot.append(
            {"start_year": year[0], "date": day, "earns": data[i]}, ignore_index=True)
    return df_plot
