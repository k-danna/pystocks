
import config as cfg
from misc import *

class Account(object):
    def __init__(self, name='testaccount'):
        self.name = name
        self.cash = cfg.start_cash
        self.networth = self.cash
        self.buypower = self.cash * cfg.risk
        self.positions = self.init_positions() #symbol: shares
        msg('using account: %s' % self.name, '+')
    
    def init_positions(self):
        positions = {}
        for symbol in cfg.tickers:
            positions[symbol] = 0
        #query api and set any current holdings
        return positions

    def update(self, date):
        #update networth
        self.networth = self.cash
        for symbol in self.positions:
            data = cfg.db.cur.execute(
                'select * from %s where Date=?' % symbol, (date,)
            )
            data = cfg.db.cur.fetchall()
            if len(data) == 0:
                continue
            AdjClose = data[0][6]
            self.networth += (self.positions[symbol] * AdjClose)

        #update buypower
        self.buypower = self.cash * cfg.risk

        #update all other class vars
        pass

    def info(self, date):
        self.update(date)
        roi = ( self.networth - cfg.start_cash) / cfg.start_cash
        print  ('[*] account info for \'%s\'\n    current networth: %s\n'
                '    initial investment: %s\n    return on investment: %s\n'
                '    positions: %s\n'
                % (self.name, self.networth, cfg.start_cash, roi, 
                   self.positions))

