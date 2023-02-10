"""
The purpose of this file is to create a csv which acts as a data source for
calculating the option information.  It is this data which will be uploaded
in the REST API.
A mature application would retrieve the data from SQL rather than a csv.
This should be regarded as mocked data rather than realistic data.
The original source of the data is https://fred.stlouisfed.org/ accessed on
February 10, 2023.  The data collected is Henry Hub Natural Gas Spot Price (DHHNGSP)
from Feb 7, 2018 to Feb 7, 2023 and Crude Oil Prices: Brent - Europe (DCOILBRENTEU) from
Feb 6, 2018 to Feb 6, 2023
The Henry Hub data acts, using the same dates and prices, as a proxy for HH futures (HH) dated
MAR 24.  The Brent data acts as a proxy for BRENT futures (BRN) dated JAN 24.
Accordingly those columns are renamed.
"""
import pandas as pd
"""
In this small-scale project, the csv files
are stored in the same directory as the 
code for ease of access.  These would
be separated in later drafts of the code.
"""
HH = pd.read_csv("DHHNGSP.csv")
BRN = pd.read_csv("DCOILBRENTEU.csv")

combined = HH.merge(BRN, left_on='DATE', right_on='DATE')
combined.sort_values(by='DATE', inplace=True)
combined.rename(columns={"DHHNGSP": "HH", "DCOILBRENTEU": "BRN"}, inplace=True)

# Inspection reveals that some data cleaning is necessary
# The value data consists of strings but some consist of just a .
# so they will simply be removed.
combined = combined[combined["BRN"] != "."]
combined = combined[combined["HH"] != "."]
combined["BRN"] = combined["BRN"].astype(float)
combined["HH"] = combined["HH"].astype(float)
combined = combined[combined["BRN"] > 0]
combined = combined[combined["HH"] > 0]
combined.to_csv("CombinedEnergyFutures.csv", index=False)

