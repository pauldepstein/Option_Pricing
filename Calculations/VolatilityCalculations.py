import numpy as np
import pandas as pd


def historicalVol(df: pd.DataFrame, ticker: str, minSample: int = 5) -> float:
    """
    A function for calculating annualized vols based
    on historical volatility as given by data
    in a dataframe.
    The dates are assumed to be sorted with values
    one business day apart. The volatility
    is calculated as the standard deviation
    of the log returns multiplied by the
    annualization factor of 260 business days
    in a year.
    :param df: dataframe containing the data,
    :param ticker: ticker string
    :param minSample: minimum sample size for
    volatility to be meaningful.
    :returns annualized volatility
    """

    if ticker not in df.columns:
        raise ValueError("The data source does not correspond to your ticker")

    if len(df) < minSample:
        raise ValueError("Not enough data to determine volatility")

    DAYS_IN_YEAR = 260
    return np.nanstd(np.log(df[ticker]).diff()) * np.sqrt(DAYS_IN_YEAR)