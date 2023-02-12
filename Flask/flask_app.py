from flask import Flask, render_template, request
import pandas as pd
from UploadData import dataFromStartDate
from Calculations.PVCalculator import PV

Flask_App = Flask(__name__)

"""
For this first draft, information about the limited choice 
in tickers is kept globally.
It is a simplifying assumption that futures are only available 6 months forward.
This is enforced via a default parameter in the PV function.
Furthermore as in the assignment, BRN options expire
2 months before delivery and HH options expire 1 month before delivery.  This
is announced in a global dictionary.

A notable feature is that the sigma for the options is calculated via historical
volatility for the dataframe and is not input by the user.
Future drafts should probably make this value less hidden, and display it to the
user, or even allow the user to input it.
"""
monthsBack = {"BRN": 2, "HH": 1}

@Flask_App.route('/', methods=['GET'])
def index():
    """
    Displays the index accessible at '/'
    :return: returns the render_template object
    """
    return render_template('index.html')

def _yesNoValidator(objectType: str, yesNo: str) -> bool:
    """
    Enforcing a yes/no validation required
    in the web form.
    Exception raised if the user types something else
    :param objectType: string that gets inserted into
    the error message so that we know which object
    did not get validated.
    :param yesNo: string that should be yes/no but
    is a potential source of user error
    :returns: True if the user typed yes and false for no
    """
    validatingDict = {'Y': True, 'N': False}
    responseIndicator = yesNo[0].upper()
    if responseIndicator not in validatingDict:
        raise ValueError(objectType + " was  not answered by yes or no.")
    else:
        return validatingDict[responseIndicator]

def _obtainDf(ticker: str) -> pd.DataFrame:
    """
    Obtaining the necessary dataframe
    which may be the one from the present csv
    or uploading may be required
    :param ticker is a string indicator of the ticker
    """
    datasource = "CombinedEnergyFutures.csv"  # string indicating where data is kept
    # Should computation be based on current dataframe
    # or is a new dataframe needed
    upload = request.form['Upload']
    # Check this was answered correctly
    upload = _yesNoValidator("upload", upload)
    return dataFromStartDate(ticker) if upload else pd.read_csv(datasource)

@Flask_App.route('/price/', methods=['POST'] )
def price():
    """Routes where we send form input"""
    # ticker selected for example "HH"
    ticker = request.form['Ticker']
    strike = request.form['Strike']
    # A call is indicated by yes below and a put
    # indicated by no.
    is_call = request.form['Call']
    # Dataframe depends on whether an upload is requested
    try:
        df = _obtainDf(ticker)
        strike = float(strike)
        # Call is true if yes, false if no and raises
        # an exception if neither
        is_call = _yesNoValidator("call_or_put", is_call)
        monthsSubtract = monthsBack[ticker] # month before delivery that option expires
        # Use the PV Calculator to do the computation
        result = PV(df, ticker, monthsBack[ticker], strike, is_call)
        return render_template(
        'index.html',
        ticker=ticker,
        is_call=is_call,
        strike = strike,
        result=result,
        PV_success=True
        )
    except ValueError as err:
        return render_template(
        'index.html',
        ticker=ticker,
        is_call=is_call,
        strike = strike,
        result='Failed',
        PV_success=False,
        error=str(err)
        )

if __name__ == '__main__':
    Flask_App.debug = True
    Flask_App.run()
