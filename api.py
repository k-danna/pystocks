
#simple wrapper for trading api

import config as cfg
from misc import *

class API(object):
    def __init__(self, interval):
        self.interval = interval
        self.key = ''
        self.secret = ''

    def buy(symbol, shares, price):
        msg('bought %s %s at %s', % (shares, symbol), '+')
        cfg.account.positions[symbol] += shares
        cfg.account.cash -= (shares * price)
        pass

    def sell(symbol, shares, price):
        msg('sold %s %s at %s', % (shares, symbol), '+')
        cfg.account.positions[symbol] -= shares
        cfg.account.cash += (shares * price)
        pass

    def flatten(symbol, price):
        shares = cfg.account.positions[symbol]
            if shares > 0:
                self.sell(symbol, shares, price)
            elif shares < 0:
                self.buy(symbol, shares, price)

    def get_account(self):
        pass

