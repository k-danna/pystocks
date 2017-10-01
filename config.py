
from datetime import datetime
from account import Account
from database import Database

#account
account = Account(1000.0)

#database
db = Database('test.db')

#load api obj, set key/secret from encrypted file

#use historical data to test algo
backtest = True
test_begin = datetime(1995, 01, 01)

#refresh rate for market ticks in seconds
tick_interval = 10.0

#target tickers for trading
tickers = ['NFLX', 'AAPL', 'NEE', 'FNB']

#cost per trade
cost = 7.95

#misc
debug = True
today = datetime.now()

