
import sys
import sqlite3 as sql

import config as cfg
from misc import *

class Database(object):
    def __init__(self, name):
        self.name = name
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
        #download csv
            #get most recent date in csv
            #if most recent != most recent in db
                #load missing data into db
                    #add days backward until one is already in there
                        #calc missing indicators
                    #add table to db
                    #check last date entered 
                    #add all entries up to now
        pass

    def query(self, statement):
        self.cur.execute(statement)
        return self.cur.fetchall()

