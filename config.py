
from datetime import datetime
from account import Account

#account
account = Account(1000.0)

#load api obj, set key/secret from encrypted file

#misc variable for breakpoints, etc
debug = True

#use historical data to test algo
backtest = True
test_begin = datetime(1995, 01, 01)

#refresh rate for market ticks in seconds
tick_interval = 10.0

#target tickers for trading
tickers = ['NFLX', 'AAPL', 'NEE', 'FNB']

#cost per trade
cost = 7.95

#connection to database
conn = 0

#misc
today = datetime.now()

