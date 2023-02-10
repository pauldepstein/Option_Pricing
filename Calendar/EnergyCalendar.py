"""
This task appears to require calendar computation.
For example, it is required to identify the last
business day of the 2nd month before the delivery month.
This file is intended to enable these computations.
No error handling is done because such error handling
is regarded as the responsibility of the web interface.
"""
import datetime
from typing import Tuple
import arrow
import pandas
import numpy as np


class EnergyCalendar:
    """Custom calendar for energy commodities trading
    Since, in this first draft, business days are just week days,
    the number of days in a year can be considered to be 52 * 5.
    """
    DAYS_IN_YEAR = 260

    def __init__(self, YearMonthDay: Tuple[int, int, int]):
        """
        :param YearMonthDay: a tuple of ints representing the
        year, month and day in that order
        Both the datetime and the date object are needed.
        """
        self.date = datetime.date(*YearMonthDay)
        self.datetime = datetime.datetime(*YearMonthDay)

    def shift(self, offset: int, period: str = "month") -> datetime.date:
        """
        Move the date forward or backward according to the offset
        and the period.  For example if the offset is 3 and the
        period is "day", we move 3 days forward.  Backward shifts
        are indicated by negative offsets.
        This first draft only allows a single shift per function call
        but an easy improvement could allow shifts of (for example)
        one month and 3 days.
        Currently this function is only being called with the default
        setting of "month".  Setting period to "day" or any other value apart
        from "month" has not been used or thoroughly tested.
        :param offset:  How many periods do we move forward?
        :param period:  The unit of time
        :return:        The corresponding date
        """
        # datetime uses singular convention and arrow uses plural convention
        # so an adjustment is needed.
        pluralPeriod = period + "s"
        arrowDate = arrow.Arrow.fromdatetime(self.datetime)

        # Now construct the dictionary and pass it to the arrow object.
        arrowDict = {pluralPeriod: offset}
        arrowDate = arrowDate.shift(**arrowDict)
        return arrowDate.datetime.date()

    def lastDayOfMonth(self, offset) -> datetime.date:
        """
        The last day of the month after moving
        forward (or backwards) the number of months specified
        in the offset.
        :param offset: Number of months
        :return: The corresponding datetime
        The strategy is to go forward one more month
        than the offset then replace the day by the first day
        of the month. Finally, step back one day.
        """
        monthsForward = self.shift(offset + 1)
        firstDay = monthsForward.replace(day=1)
        return firstDay - datetime.timedelta(days=1)

    def lastBusinessDayOfMonth(self, offset) -> datetime.date:
        """
        The last business day (non-weekend) of the month after moving the
        number of months specified in the offset.
        Future drafts of the code could be much more flexible and accurate by
        considering other periods besides months, and official holiday
        calendars like the US Federal Calendar. Currently, Christmas (for example)
        is considered a business day if it's not a weekend.
        :param offset: Number of months
        :return: The corresponding date
        """
        lastDate = self.lastDayOfMonth(offset)
        # Date needs conversion into a datetime object
        lastDatetime = datetime.datetime(lastDate.year, lastDate.month, lastDate.day)
        # The most usual case is that this last day is already a business day
        # Otherwise keep stepping one day back until we reach a business day
        bday = pandas.tseries.offsets.BDay()
        is_business_day = bday.is_on_offset(lastDatetime)
        while not is_business_day:
            lastDay = lastDay - datetime.timedelta(days=1)
            is_business_day = bday.is_on_offset(lastDatetime)
        return lastDatetime.date()

    def lastBusinessDayEnergy(self, ticker: str) -> datetime.date:
        """
        Covering the special case of Brent and Henry Hub options.
        Henry Hub is indicated by HH and Brent is the default
        Other commodities are not considered in this first draft
        but should be added later.
        Brent option expiry is the last business day of the second
        month before the delivery month and Henry Hub option expiry
        is on the last business day of the month before the delivery
        month.
        The delivery date comes from the class member.
        :param ticker: Commodity string which can only be HH or BRN in
                       this first draft
        :returns option expiry date as given above.
        """
        if ticker == "HH":
            return self.lastBusinessDayOfMonth(-1)
        if ticker == "BRN":
            return self.lastBusinessDayOfMonth(-2)
        print("This ticker is not yet implemented -- Brent default is assumed")
        return self.lastBusinessDayOfMonth(-2)


