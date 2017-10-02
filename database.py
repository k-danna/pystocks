
import sys
import sqlite3

from misc import *

class Database(object):
    def __init__(self, name):
        self.name = name
        try:
            self.con = sqlite3.connect(self.name)
            self.cur = self.con.cursor()
            #print self.query('select sqlite_version()')
            
            #make sure db has correct data / correct tables
                #download and load if not

        except:
            #create db
            #for each file in db folder
                #add table to db

            #for now just error
            msg('could not connect to database: %s' % self.name, '-')
            sys.exit(1)
    
    def get_data(self, symbol):
        #download csv
        #load into dAb

    def query(self, statement):
        self.cur.execute(statement)
        return self.cur.fetchall()

