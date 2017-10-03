
import config as cfg

class Account(object):
    def __init__(self, name='testaccount'):
        self.name = name
        self.cash = cfg.start_cash
        self.networth = self.cash
        self.buypower = self.cash * cfg.risk
        self.positions = self.init_positions() #symbol: shares
        self.update()
    
    def init_positions(self):
        positions = {}
        for symbol in positions:
            positions[symbol] = 0
        #query api and set any current holdings
        return positions

    def update(self):
        #FIXME: query api for balances, open positions and do math
        #update all class vars
        #self.networth = total
        #update buypower, etc
        pass

    def info(self):
        self.update()
        roi = ( self.networth - cfg.start_cash) / cfg.start_cash
        print  ('[*] account info for \'%s\'\n    current networth: %s\n'
                '    initial investment: %s\n    return on investment: %s\n'
                % (self.name, self.networth, cfg.start_cash, roi))

