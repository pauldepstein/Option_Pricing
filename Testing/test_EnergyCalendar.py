import unittest
import datetime
from Calendar.EnergyCalendar import EnergyCalendar


class TestEnergyCalendar(unittest.TestCase):
    """
    A class to test the calendar computations in EnergyCalendar
    The information in the assignment document is tested here.
    The Jan and March 24 options will be dated Jan 1, 2024 and March 1, 2024
    A BRN Jan-24 option is a European option with underlying ICE Brent Jan-24 Future.
    BRN option expiry will be the last business day of the 2nd month before the delivery month.
    For example, BRN Jan-24 expiry date is 2023-11-30.
    HH Mar24 option is a European option with underlying Henry Hub Gas March 24 Future contract.
    HH option expiry is the last business day of the month before the delivery month.
    For example, HH Mar-24 expiry date is 2024-02-29.
    """
    def test_HH(self):
        """Testing Henry Hub"""
        date = (2024, 3, 1) # March 1, 2024 represented as a tuple of ints
        HHDate = EnergyCalendar(date)
        expectedExpiry = datetime.date(2024, 2, 29) # given in assignment doc
        self.assertEqual(HHDate.lastBusinessDayEnergy("HH"), expectedExpiry)

    def test_Brent(self):
        """Testing ICE Brent"""
        date = (2024, 1, 1) # January 1, 2024 represented as a tuple of ints
        BRNDate = EnergyCalendar(date)
        expectedExpiry = datetime.date(2023, 11, 30) # given in assignment doc
        self.assertEqual(BRNDate.lastBusinessDayEnergy("BRN"), expectedExpiry)


if __name__ == '__main__':
    unittest.main()
