import numpy as np
import pandas as pd


def historicalVol(df: pd.DataFrame, ticker: str, minSample: int = 5) -> float:
    """
    A function for calculating annualized vols based
    on historical volatility as given by data
    in a dataframe.
    A mature application would use exceptions.
    However, this first draft assumes the data
    is valid, trusting my visual inspection and
    data cleaning.
    For some easily determined errors, -1
    is returned as a sentinel value, with a message
    displayed.
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
        print("The dataframe does not correspond to your ticker")
        return -1

    if len(df) < minSample:
        print("Not enough data to determine volatility")
        return -1

    DAYS_IN_YEAR = 260
    return np.nanstd(np.log(df[ticker]).diff()) * np.sqrt(DAYS_IN_YEAR)