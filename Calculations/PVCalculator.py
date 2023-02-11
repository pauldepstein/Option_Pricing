from OptionsCalculator import OptionsCalculator
from VolatilityCalculations import historicalVol
from Calendar.CalendarComputations import timeBetween
from Calendar.EnergyCalendar import EnergyCalendar
import pandas as pd
import numpy as np
import datetime


def PV(df: pd.DataFrame, ticker: str, monthsBack: int, strike: float, isCall: bool, rate: float = 0.05, monthsForward: int = 6 ) -> float:
    """
    Use the OptionsCalculator class together with the Calendar class to compute the PV of the options
    :param: df is the DataFrame containing the price.  This is used for both the current value of the future and
    the historical vol calculations.
    :param: ticker is the ticker string
    :param: monthsBack is the number of months before the delivery date that the option expires
    :param: strike
    :param: rate is the interest rate defaulted to 5% which is standard in simple applications
    :param: monthsForward is the number of months forward from now that the delivery date occurs.
    :param isCall is true for a call and false for a put
    For example, if now is February 23, then a delivery date in April 23 would be two months forward.
    To simplify early versions of the web form, user input is minimised and therefore a default value of
    6 months forward is preset.
    Standard quant notation is used for all parameters.
    No formal testing (other than user observations) but the earlier functions have been unit-tested.
    """
    if not ticker in df.columns:
        raise ValueError("Can not price -- inconsistent information")

    if strike <= 0:
        raise ValueError("Strike must be positive")

    # Present value of future is final entry of dataframe
    K = df[ticker].iloc[-1]
    print("K =", K)
    if K <= 0:
        raise ValueError("Value of future must be positive")
    # Sigma comes form historical volatilities
    sigma = historicalVol(df, ticker)
    print("The value of sigma is", sigma)
    if sigma < 0 or np.isnan(sigma):
        raise ValueError("Can not price -- error found in sigma")

    # Use the calendar to find T -- the time to expiry
    # First consider the beginning of the current month
    today = datetime.datetime.now().date()
    # EnergyCalendar is constructed via a tuple
    todaytuple = tuple(today.timetuple())[0:3]
    calendar = EnergyCalendar(todaytuple)
    # For the expiry time, we shift monthsForward months
    # forward when considering the delivery date and then
    # monthsBack months back.
    combinedShift = monthsForward - monthsBack
    expiryDate = calendar.lastBusinessDayOfMonth(combinedShift)
    # The expiry date is crucial information which should be
    # given to the user.  A more sophisticated application
    # would do something more than just a raw print statement.
    print("The expiry date is", expiryDate)
    T = timeBetween(today, expiryDate)
    print("T is", T)
    if T < 0:
        raise ValueError("Error -- time to expiry can not be negative")

    # Now all the elements are in place to price via the option calculator
    option = OptionsCalculator(sigma, T, K, strike, rate)
    return option.Black76(isCall)
