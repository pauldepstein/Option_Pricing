import unittest
import datetime
from Calendar.CalendarComputations import timeBetween


class TestCalendarComputations(unittest.TestCase):
    """
    Testing the computations in the CalendarComputations file
    Expected result comes from accessing
    https://www.timeanddate.com/date/workdays.html?d1=1&m1=3&y1=2021&d2=7&m2=08&y2=2021&ti=on&
    on Feb 9, 2023
    """
    def test_timeBetween(self):
        firstDate = datetime.date(2021, 3, 1)
        secondDate = datetime.date(2021, 8, 7)
        expectedResult = 115/260
        actualResult = timeBetween(firstDate, secondDate)
        print(actualResult)
        print(expectedResult)
        self.assertAlmostEqual(actualResult, expectedResult)


if __name__ == '__main__':
    unittest.main()
