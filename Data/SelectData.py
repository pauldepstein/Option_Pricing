"""
Selecting data for uploading from the original data source -- CombinedEnergyFutures.csv
The user will certainly want the most recent data.
However, this code provides flexibility as to how far back in history, the user wants to go.
Those rows are then selected and returned as a dataframe.
Furthermore, the only prices returned are those from the ticker requested by the user.
"""
import datetime
import pandas as pd

file = "CombinedEnergyFutures.csv" # Same directory so full path not needed
tickers = ["HH", "BRN"]

def dataFromStartDate(date: datetime.date, ticker: str) -> pd.DataFrame:
    """
    Provide all energy futures data at or later than the date
    requested by the user and for the ticker required.
    :param date: datetime.date for the earliest data requested by the user
    :param ticker: string indicating commodity indicated by the user
    :return: dataframe with user data.
    """
    if ticker not in tickers:
        # Could use exceptions in a more mature version
        print("This ticker is not currently available")
        return pd.DataFrame()

    fullData = pd.read_csv(file)
    recentData = fullData[fullData['DATE'] >= date.strftime('%Y-%m-%d')]
    tickerData = recentData[['DATE', ticker]]
    return tickerData
