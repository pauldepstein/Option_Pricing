import unittest
import numpy as np
import pandas as pd
from Calculations.VolatilityCalculations import historicalVol


class TestVolatility(unittest.TestCase):
    def test_volatility(self):
        """
        Testing the historicalVol function.
        Create a simple dataframe by hand and
        check that the volatility matches hand computations.
        """
        DAYS_IN_YEAR = 260 # Business days in year
        data = [1, np.exp(2), 1]
        # The log diffs are 2 and -2 leading to
        # a standard deviation of 2.  This gets multiplied
        # by the sqrt of 260
        df = pd.DataFrame(data, columns=['HH'])
        # In the default setting, such small dataframes
        # are not accepted so minSample is set to 3
        actual = historicalVol(df, "HH", 3)
        expected = 2 * np.sqrt(DAYS_IN_YEAR)
        self.assertAlmostEqual(actual, expected)

    def test_volatility_error(self):
        """
        Testing historicalVol for the exceptions
        handling case where the ticker was not entered correctly.
        The error string is checked.
        """
        data = [1, 1, 1, 1, 1]
        df = pd.DataFrame(data, columns=['HH'])
        expected = "The data source does not correspond to your ticker"

        try:
            vol = historicalVol(df, "BRN", 3)
        except ValueError as error:
            self.assertEqual(str(error), expected)
            return None

        self.assertEqual(True, False) # We should not be in this block as an exception should have been raised.

if __name__ == '__main__':
    unittest.main()
