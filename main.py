#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True

import time
from datetime import datetime

import config as cfg
import backtest as bt
from misc import *

def main():
    #general init
    #load api obj, set key/secret from encrypted file

    #query api for balances, open positions, etc
    msg('getting account details')
    cfg.account.update()
    #cfg.account.info()

    #backtest algorithm
    msg('beginning backtest\n')
    if cfg.backtest:
        bt.backtest()
        msg('done testing')
        cfg.account.info()

    #msg('monitoring specified symbols')
    #for each symbol in cfg.tickers
        #analyze (calc and eval)
        #create trade for each and trade the best one if able to
        #loop on tick interval

if __name__ == '__main__':
    main()

