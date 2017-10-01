
class Account(object):
    def __init__(self, investment, name='testaccount'):
        self.name = name
        self.investment = investment
        self.networth = self.investment
        self.cash = self.investment
        self.buypower = self.cash * 0.3
        self.open_positions = {'NFLX': 0} #symbol: shares
        self.update()
    
    def update(self):
        #FIXME: query api for balances, open positions and do math
        #self.networth = total
        pass

    def info(self):
        self.update()
        roi = ( self.networth - self.investment) / self.investment
        print  ('[*] account info for \'%s\'\n    current networth: %s\n'
                '    initial investment: %s\n    return on investment: %s\n'
                % (self.name, self.networth, self.investment, roi))

