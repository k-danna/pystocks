
from datetime import datetime
from account import Account
from database import Database

from misc import *

#program info
prog_name = 'pystocks'
prog_version = '0.0.1'
welcome = '%s v%s\n' % (prog_name, prog_version)

#on-start message
msg(welcome, sym=False)
msg('initializing program')

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

#init account
account = Account(1000.0)

#init database
db = Database('test.db')

#load api obj, set key/secret from encrypted file

