
import sys
import csv
import sqlite3 as sql

import config as cfg
from misc import *

class Database(object):
    def __init__(self, name):
        self.name = 'data/%s' % name
        try:
            self.con = sql.connect(self.name)
            self.cur = self.con.cursor()
            #print self.query('select sqlite_version()')
            msg('connected to db: %s' % self.name, '+')
            
            #make sure db has correct data / correct tables

        except:
            #error and exit for now
            msg('could not connect to database: %s' % self.name, '-')
            sys.exit(1)

        #add or update specified symbols
        for symbol in cfg.tickers:
            self.update_symbol(symbol)
    
    def update_symbol(self, symbol):
        msg('updating data: %s' % symbol)
        #FIXME: auto download csv and only add new data
        #add new table if neccessary
        #get most recent weekday date
        #get most recent date in csv
            #add missing data
            #calc missing indicators
        
        #for now just remake the whole db
        #add quotes
        self.cur.execute((
            ('create table if not exists %s (' % symbol) +
            'id integer primary key autoincrement,'
            'Date text unique not null,'
            'Open real not null,'
            'High real not null,'
            'Low real not null,'
            'Close real not null,'
            'AdjClose real not null,'
            'Volume real not null'
            ')'
        ))
        reader = csv.reader(open('data/%s.csv' % symbol, 'rb')) 
        next(reader) #skip header
        for Date, Open, High, Low, Close, AdjClose, Volume in reader:
            self.cur.execute((
                'insert or ignore into %s ' % symbol + 
                '(Date, Open, High, Low, Close, AdjClose, Volume)'
                'values (?,?,?,?,?,?,?)'), (Date, Open, High, Low, Close, 
                        AdjClose, Volume)
            )

        #add splits
        s = '_splits'
        self.cur.execute(
            'create table if not exists %s%s (' % (symbol, s) +
            'id integer primary key autoincrement,'
            'Date text unique not null,'
            'Split text not null'
            ')'
        )
        reader = csv.reader(open('data/%s%s.csv' % (symbol, s), 'rb')) 
        next(reader) #skip header
        for Date, Split in reader:
            self.cur.execute((
                'insert or ignore into %s%s ' % (symbol, s) + 
                '(Date, Split)'
                'values (?,?)'), (Date, Split)
            )
        
        #add dividends
        s = '_dividends'
        self.cur.execute(
            'create table if not exists %s%s (' % (symbol, s) +
            'id integer primary key autoincrement,'
            'Date text unique not null,'
            'Dividend real not null'
            ')'
        )
        reader = csv.reader(open('data/%s%s.csv' % (symbol, s), 'rb')) 
        next(reader) #skip header
        for Date, Dividend in reader:
            self.cur.execute((
                'insert or ignore into %s%s ' % (symbol, s) +
                '(Date, Dividend)'
                'values (?,?)'), (Date, Dividend)
            )
        

    def query(self, statement):
        self.cur.execute(statement)
        return self.cur.fetchall()


#
# finance new api now requires cookies
#https://stackoverflow.com/questions/44105187/error-in-downloading-csv-from-new-yahoo-finance-historical-data
#https://github.com/dennislwy/YahooFinanceAPI
#

