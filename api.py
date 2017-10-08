
from datetime import datetime

import config as cfg
import analyze
from misc import msg

class API(object):
    def __init__(self):
        msg('connected to api', '+')
        self.account = Account()

    def buy(self, symbol, shares, price, date):
        #FIXME: output to log file 
        msg('%s BUY %s %s@%s' % (date, symbol, shares, price), ind=1)
        position, _, _ = self.account.positions[symbol]
        self.account.cash -= cfg.commission
        self.account.cash -= (shares * price)
        self.account.positions[symbol] = (position + shares, price, date)

        self.account.update(date)

    def sell(self, symbol, shares, price, date):
        #FIXME: output to log file
        msg('%s SELL %s %s@%s' % (date, symbol, shares, price), ind=1)
        position, prev_price, prev_date = self.account.positions[symbol]
        self.account.cash -= cfg.commission
        self.account.cash += (shares * price)
        self.account.positions[symbol] = (position - shares, price, date)
        self.account.trades[symbol].append((prev_date, date, prev_price, 
                price, shares))
        
        self.account.update(date)

    def flatten(self, symbol, price, date):
        shares = self.account.positions[symbol][0]
        if shares > 0:
            self.sell(symbol, shares, price, date)
        elif shares < 0:
            self.buy(symbol, -shares, price, date)

    def reverse(self, symbol, price, date):
        shares = self.account.positions[symbol][0]
        if shares > 0:
            self.sell(symbol, shares, price, date)
            self.buy(symbol, shares, price, date)
        elif shares < 0:
            self.buy(symbol, -shares, price, date)
            self.sell(symbol, -shares, price, date)

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

    def account_stats(self, date):
        #FIXME: calc all stats and call info
        pass

    def update_account(self, date):
        self.account.update(date)

    def reset_account(self):
        self.account = Account()


class Account(object):
    def __init__(self, name='testaccount'):
        self.name = name
        self.cash = cfg.start_cash
        self.networth = self.cash
        self.buypower = self.cash * cfg.risk
        self.positions = self.init_positions() #symbol: shares
        self.trades = self.init_trades() # symbol: [(date_bought, 
                #date_sold, price_bought, price_sold, shares), ...]
        msg('using account: %s' % self.name, '+')
    
    def init_trades(self):
        trades = {}
        for symbol in cfg.tickers:
            trades[symbol] = []
        return trades

    def init_positions(self):
        positions = {}
        for symbol in cfg.tickers:
            positions[symbol] = (0, 0.0, '') #(shares, price, date)
        #query api and set any current holdings
        return positions

    def update(self, date):
        #update networth
            #query and add all open position values to balance
        self.networth = self.cash
        for symbol in self.positions:
            data = cfg.db.cur.execute(
                'select * from %s where Date=?' % symbol, (date,)
            )
            data = cfg.db.cur.fetchall()
            if len(data) == 0:
                continue
            AdjClose = data[0][6]
            self.networth += (self.positions[symbol][0] * AdjClose)

        #update buypower
        self.buypower = self.cash * cfg.risk

    def init_stats(self):
        stats = {}
        self.stat_listing = [ 'inital_investment','networth','roi',
                #'avg_trades_symbol','min_trades_symbol',
                #'max_trades_symbol',
                'avg_profit','min_profit','max_profit',
                'total_trades','good_trades','bad_trades','good/bad ratio',
                'avg_trade_len','min_trade_len','max_trade_len',
                #'avg_profit_yearly','min_profit_yearly',
                #'max_profit_yearly',
                #'exposure','risk_adj_return'
        ]
        for stat in self.stat_listing:
            stats[stat] = 0.0
        return stats

    def calc_stats(self):
        stats = self.init_stats()

        #iterate through all trades made
        profits = []
        trade_counts = []
        trade_lengths = []
        for symbol in self.trades:
            #track trade counts
            trade_counts.append(float(len(self.trades[symbol])))
            for date_bought, date_sold, price_bought, price_sold, \
                    shares in self.trades[symbol]:
                
                #track profits
                profit = ((shares * price_sold - shares * price_bought) 
                        - 2 * cfg.commission)
                profits.append(profit)
                msg('%s %s %s' % (date_sold, symbol, profit), c=(
                        '+' if profit > 0 else '-'))
                
                #track trade timeframes
                sold = datetime.strptime(date_sold, '%Y-%m-%d')
                bought = datetime.strptime(date_bought, '%Y-%m-%d')
                trade_lengths.append((sold - bought).days)

        #calc account based stats
        stats['inital_investment'] = cfg.start_cash
        stats['networth'] = self.networth
        stats['roi'] = ( self.networth - cfg.start_cash) / cfg.start_cash
        stats['total_trades'] = sum(trade_counts)
        
        #dont calc anything if no trades took place
        if stats['total_trades'] == 0:
            return stats

        #calc trade count stats
        #stats['min_trades_symbol'] = min(trade_counts)
        #stats['max_trades_symbol'] = max(trade_counts)
        #stats['avg_trades_symbol'] = sum(trade_counts) / len(trade_counts)
        stats['good_trades'] = float(len([x for x in profits if x > 0.0]))
        stats['bad_trades'] = float(len([x for x in profits if x <= 0.0]))
        stats['good/bad ratio'] = stats['good_trades'] / stats['bad_trades']
        
        #calc profit stats
        stats['min_profit'] = min(profits)
        stats['max_profit'] = max(profits)
        stats['avg_profit'] = sum(profits) / len(profits)
        
        #calc timeframe stats
        stats['min_trade_len'] = min(trade_lengths)
        stats['max_trade_len'] = max(trade_lengths)
        stats['avg_trade_len'] = sum(trade_lengths) / len(trade_lengths)

        return stats

    def info(self, date):
        self.update(date)
        stats = self.calc_stats()
        msg('account info for \'%s\'' % self.name)
        for stat in self.stat_listing:
            msg('%20s: %s' % (stat, stats[stat]), ind=1)

