import numpy as np
import scipy.stats as stats


class OptionsCalculator:
    """Calculate option prices and Greeks"""

    def __init__(self, sigma: float, time: float, price: float, strike: float, rate: float = 0.05):
        """
        Option Parameters

        Args:
        sigma: annualized volatility
        time:  time to expiry in years
        price: current price of asset in USD
        strike: strike in USD
        rate:  US interest rate set to 5% for ease of computation.
        Federal Reserve rate was actually 4.5% on February 8, 2023
        """
        self.sigma = sigma
        self.time = time
        self.price = price
        self.strike = strike
        self.rate = rate

    def Black76(self, is_call: bool) -> float:
        """A formula for pricing options on futures
        Currently, the reference is https://en.wikipedia.org/wiki/Black_model
        but a more authoritative reference can be given in future drafts

        Arg:
            is_call is True when option is a call and false for a put
        Returns:
            Present value of option

        Using standard notation, the value of a call is exp(-rT) * (FN(d1) - KN(d2))
        and the value of a put is exp(-rT) * (KN(-d2) - FN(-d1))
        """
        def call(_discount: float, _F: float, _K: float, _Nd1: float, _Nd2: float) -> float:
            """
            Nested functions for calls and puts compute the values assuming some intermediate values have
            already been computed
            :param _discount: This is exp(-rT) discounting the future payment to the present
            :param _F: The value of the future
            :param _K: The strike rate
            :param _Nd1: A normcdf value expressed in standard notation
            :param _Nd2: A normcdf value expressed in standard notation
            :return: The fair value of the call option
            """
            return _discount * (_F * _Nd1 - _K * _Nd2)

        def put(_discount: float, _F: float, _K: float, _Nd1: float, _Nd2: float) -> float:
            """
            The fair value for puts using the same parameters as in the case of calls.
            Note that N(-x) = 1 - N(x)
            """
            Nminus_d1, Nminus_d2 = 1 - _Nd1, 1 - _Nd2
            return discount * (_K * Nminus_d2 - _F * Nminus_d1)

        def d1(_F: float, _K: float, sigma: float, time: float) -> float:
            """
            The d1 value, as in standard financial mathematics
            is computed.  Parameter names are as previously stated.
            """
            ratio = _F / _K
            logRatio = np.log(ratio)
            addVol = logRatio + time * sigma * sigma / 2
            return addVol/(sigma * np.sqrt(time))

        # The value of the future is akin to the value of the asset
        d1_value = d1(self.price, self.strike, self.sigma, self.time)
        d2_value = d1_value - self.sigma * np.sqrt(self.time)
        Nd1, Nd2 = stats.norm.cdf(d1_value), stats.norm.cdf(d2_value)

        discount = np.exp(-self.rate * self.time)

        # Now we have all the steps in place to just use the formula depending on whether we have
        # a call or a put.
        if is_call:
            return call(discount, self.price, self.strike, Nd1, Nd2)
        return put(discount, self.price, self.strike, Nd1, Nd2)
