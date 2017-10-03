
#simple wrapper for trading api

import config as cfg
from misc import *

class API(object):
    def __init__(self, interval):
        self.interval = interval
        msg('connected to api', '+')

    def buy(self, symbol, shares, price, date):
        msg(date)
        msg('bought %s %s at %s' % (shares, symbol, price), '+', ind=1)
        cfg.account.cash -= cfg.commission
        cfg.account.cash -= (shares * price)
        cfg.account.positions[symbol] += shares

        cfg.account.update(date)

    def sell(self, symbol, shares, price, date):
        msg(date)
        msg('sold %s %s at %s' % (shares, symbol, price), '+', ind=1)
        cfg.account.cash -= cfg.commission
        cfg.account.cash += (shares * price)
        cfg.account.positions[symbol] -= shares
        
        cfg.account.update(date)

    def flatten(self, symbol, price, date):
        shares = cfg.account.positions[symbol]
        if shares > 0:
            self.sell(symbol, shares, price, date)
        elif shares < 0:
            self.buy(symbol, shares, price, date)

    def get_balance(self):
        pass

