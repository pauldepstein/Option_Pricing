import unittest
import numpy as np
from Calculations.OptionsCalculator import OptionsCalculator


class TestBlack76(unittest.TestCase):
    """
    A class to test the Black 76 implementation in the
    Options Calculator.
    Tests are of the below categories:
    1. If the strike is massively larger than the futures value,
    the call price should be close to 0, and the put price should
    be close to the discounted value of (Strike - Futures value)

    2. If the futures value is massively larger than the strike,
    the call price should be close to the discounted value of (Futures Value - Strike),
    and the put price should be close to zero.

    3. I accessed https://medium.com/@polanitzer/black-1976-model-in-python-predict-european-option-prices-on-bonds-commodities-and-futures-6bca56c2e6ac
    on February 9, 2023.  This article is by Roi Polanitzer.
    He gives two worked examples which are tested here for comparison.
    """
    def setUp(self):
        """
        For simplicity for this first draft, some
        of the parameters are fixed for all unit tests
        """
        self.sigma = 0.2 # Volatility at 20% annually
        self.time = 1.5 # 1.5 years to expiry
        # The default value -- rate = 5% is used throughout

    def test_call_strike_large(self):
        """Call option -- large strike.  See 1. above"""
        strike = 1000.0
        futurePrice = 1.0

        option = OptionsCalculator(self.sigma, self.time, futurePrice, strike)
        callValue = option.Black76(True) # True for calls and false for puts
        self.assertAlmostEqual(callValue, 0.0)

    def test_put_strike_large(self):
        """Put option -- large strike.  See 1. above"""
        strike = 1000.0
        futurePrice = 1.0

        option = OptionsCalculator(self.sigma, self.time, futurePrice, strike)
        discount = np.exp(-option.rate * self.time)
        expected = discount * (strike - futurePrice)
        putValue = option.Black76(False) # True for calls and false for puts
        print("Option priced at", putValue)
        self.assertAlmostEqual(putValue, expected)

    def test_call_strike_small(self):
        """Call option -- small strike.  See 2. above"""
        strike = 1.0
        futurePrice = 1000.0

        option = OptionsCalculator(self.sigma, self.time, futurePrice, strike)
        option = OptionsCalculator(self.sigma, self.time, futurePrice, strike)
        discount = np.exp(-option.rate * self.time)
        expected = discount * (futurePrice - strike)
        callValue = option.Black76(True) # True for calls and false for puts
        print("Option priced at", callValue)
        self.assertAlmostEqual(callValue, expected)

    def test_put_strike_small(self):
        """Put option -- small strike.  See 2. above"""
        strike = 1.0
        futurePrice = 1000.0

        option = OptionsCalculator(self.sigma, self.time, futurePrice, strike)
        putValue = option.Black76(False) # True for calls and false for puts
        self.assertAlmostEqual(putValue, 0.0)

    def test_call_Polanitzer(self):
        """Polanitzer's example of a call option.  See 3. above"""
        futurePrice = 42.0
        strike = 42.0
        PolanitzerValue = 3.7982

        option = OptionsCalculator(self.sigma, self.time, futurePrice, strike)
        callValue = option.Black76(True) # True for calls and false for puts
        self.assertAlmostEqual(callValue, PolanitzerValue, 4)

    def test_put_Polanitzer(self):
        """Polanitzer's example of a call option.  See 3. above"""
        futurePrice = 42.0
        strike = 42.0
        PolanitzerValue = 3.7982

        option = OptionsCalculator(self.sigma, self.time, futurePrice, strike)
        putValue = option.Black76(False) # True for calls and false for puts
        self.assertAlmostEqual(putValue, PolanitzerValue, 4)


if __name__ == '__main__':
    unittest.main()
