# A file to do date computations.  Perhaps not needed at this stage but likely to become
# necessary as the task grows in scope.
import numpy as np
import datetime


def timeBetween(date_1: datetime.date, date_2: datetime.date) -> float:
    """Computing the time in years that lies between two dates"""
    DAYS_IN_YEAR = 260 # Number of business days in a year.
    # In a more mature application this variable would be made
    # globally accessible.
    return np.busday_count(date_1, date_2)/DAYS_IN_YEAR