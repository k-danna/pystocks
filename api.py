
#simple wrapper for trading api

import config as cfg
import analyze
from misc import msg

class API(object):
    def __init__(self):
        msg('connected to api', '+')
        self.account = Account()

    def buy(self, symbol, shares, price, date):
        msg(date)
        msg('bought %s %s at %s' % (shares, symbol, price), '+', ind=1)
        self.account.cash -= cfg.commission
        self.account.cash -= (shares * price)
        self.account.positions[symbol] += shares

        self.account.update(date)

    def sell(self, symbol, shares, price, date):
        msg(date)
        msg('sold %s %s at %s' % (shares, symbol, price), '+', ind=1)
        self.account.cash -= cfg.commission
        self.account.cash += (shares * price)
        self.account.positions[symbol] -= shares
        
        self.account.update(date)

    def flatten(self, symbol, price, date):
        shares = self.account.positions[symbol]
        if shares > 0:
            self.sell(symbol, shares, price, date)
        elif shares < 0:
            self.buy(symbol, shares, price, date)

    def reverse(self, symbol, price, date):
        shares = self.account.positions[symbol]
        if shares > 0:
            self.sell(symbol, shares, price, date)
            self.buy(symbol, shares, price, date)
        elif shares < 0:
            self.buy(symbol, shares, price, date)
            self.sell(symbol, shares, price, date)

    def close_all(self, date):
        for symbol in cfg.tickers:
            price = analyze.Analyze(symbol, date).price
            self.flatten(symbol, price, date)
        pass

    def account_balance(self):
        return self.account.cash
    
    def account_networth(self):
        return self.account.networth

    def account_buypower(self):
        return self.account.buypower

    def account_positions(self):
        return self.account.positions

    def account_info(self, date):
        self.account.info(date)

    def update_account(self, date):
        self.account.update(date)


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

