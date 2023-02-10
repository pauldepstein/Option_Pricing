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
        Testing historicalVol for the error case
        where the ticker was not entered correctly.
        """
        data = [1, 1, 1, 1, 1]
        df = pd.DataFrame(data, columns=['HH'])
        actual = historicalVol(df, "BRN", 3)
        expected = -1
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
