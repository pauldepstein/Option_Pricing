The project specifics are in the asterisked section at the bottom of this page.
At this early stage, this project is basically a proof of concept, rather than
a market-ready tool to get accurate option prices.
The limitations are as follows:
1) Only HH (Henry Hub) and Brent (BRN) are available.
2) Since I do not have access to futures data, I relied on spot data as a proxy
for futures prices. The original source of the proxy data is https://fred.stlouisfed.org/ accessed on
February 10, 2023.  The data collected is Henry Hub Natural Gas Spot Price (DHHNGSP)
from Feb 7, 2018 to Feb 7, 2023 and Crude Oil Prices: Brent - Europe (DCOILBRENTEU) from
Feb 6, 2018 to Feb 6, 2023
The Henry Hub data acts, using the same dates and prices, as a proxy for HH futures (HH) 
The Brent data acts as a proxy for BRENT futures (BRN).
3) The final day for which data has been collected (Feb 6 or Feb 7, 2023) is assumed to be the
date that the API is used with the final (most recent) data representing the current Future value.
4) Futures are always assumed to be deliverable 6 months forward from the current date (Feb 6 or 7, 2023).
5) Interest rate is assumed to be constant at 5%.
6) Volatility used is historical volatility, rather than the theoretically correct implied volatility.
7) The only upload currently available is the opportunity to upload all available data for a given ticker
from 180 days from the present to the most recent date.
8) The only uploaded data available is that from the most recent upload.  The uploading process replaces
the data instead of adding to it.

User instructions
1) pip install -r requirements.txt where the requirements.txt file is in the same folder as this README.
2) Run the script flask_app.py which is agin in the same folder.
3) After a few seconds, access the URL http://127.0.0.1:5000/price/
4) Fill in the boxes as described below:
5) Yes for the upload box means that you want to upload data from up to six months in the past and price
your option according to the corresponding historical volatility.  No for the upload box means that
you want your option to be priced according to the historical volatility calculated over the entire
data set (less accurate).
6) Note that the upload option results in data being available (uploaded) in the file named "Ticker Data.csv" 
7) In the Call box, type Yes for a call or No for a put.
8) In the ticker box, type HH or BRN (the only choices currently available).  HH is for Henry Hub natural Gas
Futures and BRN is for BRENT OIL.
9) For the Strike value, in order to get meaningful results, it should be noted that the current values of
the futures are 2.17 for HH and 80.48 for BRN.
10) The volatilities are historic depending on the uploaded data, and therefore users do not enter the sigma.
11) Upon submission (Submit button), the user sees the option price displayed.
12) If the user types an error in the form, the user sees the user error explained.  Of course, pricing
is impossible with user errors.
13) The RESET button resets the user information.

*******************************************************************************************
Assignment: Implement a REST API web application for option pricing and market data storage
(recommended timing: 2-3 hours)

Features:
    1. Upload market data required for option pricing
    2. Retrieve previously uploaded market data
    3. Calculate PV of options with Black76 formula using previously uploaded market data
 
Examples of options:
BRN Jan24 Call Strike 100 USD/BBL
HH Mar24 Put Strike 10 USD/MMBTu
 
A note on the contract notation. A BRN Jan-24 option is a European option with underlying ICE Brent Jan-24 Future. BRN option expiry will be the last business day of the 2nd month before the delivery month. For example, BRN Jan-24 expiry date is 2023-11-30.
HH Mar24 option is a European option with underlying Henry Hub Gas March 24 Future contract. HH option expiry is the last business day of the month before the delivery month. For example, HH Mar-24 expiry date is 2022-02-29.

You have a freedom to choose technology stack, architecture, input/output schemas to best fit the requirements.
 
The code and design should meet these requirements, but be sufficiently flexible to allow future changes. The code should be well structured, commented, have error handling and be tested.

    • Produce working, object-oriented source code.
    • Provide as a GitHub project or send back in electronic format.
    • We will walk through your code together in the next session, answering questions on the code and programming/design choices you made.
    • At the interview you will be asked to present an end-to-end demo of the application.
********************************************************************************************************************************************************************************************************************************************************************