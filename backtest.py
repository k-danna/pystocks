
from dateutil import rrule
from datetime import datetime, timedelta

import analyze as lyz
import config as cfg
from misc import *

def backtest():
    #make sure historical data is in database
        #error, exit if not

    #iterate through weekdays since cfg.test_begin
    evals = {}
    for day in rrule.rrule(rrule.DAILY, dtstart=cfg.test_begin, 
            until=cfg.today):

        #skip weekends
        if day.weekday() > 4:
            continue

        msg(day)

        #query current, prevs days info
            #if dne calc and insert
        for symbol in cfg.tickers:
            obj = lyz.Analyze(symbol)
            evals[symbol] = obj.evaluation
        #choose best evaluation and trade if able to

def get_data(symbol):
    return 0



#INFO: iterate through year
#https://stackoverflow.com/questions/153584/how-to-iterate-over-a-timespan-after-days-hours-weeks-and-months-in-python#155172

#INFO: best way to format queries
#https://stackoverflow.com/questions/5243596/python-sql-query-string-formatting

