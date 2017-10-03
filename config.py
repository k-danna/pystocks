
from datetime import datetime
from account import Account
from database import Database

from misc import *

#program info
prog_name = 'pystocks'
prog_version = '0.0.1'

#welcome message
today = datetime.now()
welcome = '%s v%s (%s)\n' % (prog_name, prog_version, today)

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

#misc vars, cost per trade
start_cash = 3000
risk = 0.3
cost = 7.95

#misc
debug = True

#init account
account = Account()

#init database
db = Database('test.db')

#load api obj, set key/secret from encrypted file

