#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True

import time
from datetime import datetime

import config as cfg
from backtest import train, test
from misc import msg

def main():
    #general init done on config import

    #train weights
    if cfg.train:
        msg('beginning to train\n', '+')
        train()
        msg('done training', '+')

    #backtest algorithm
    if cfg.backtest:
        msg('beginning backtest\n', '+')
        test()
        msg('done testing', '+')
        cfg.api.account_info(cfg.today)

    #msg('monitoring specified symbols')
    #for each symbol in cfg.tickers
        #analyze (calc and eval)
        #create trade for each and trade the best one if able to
        #loop on tick interval

if __name__ == '__main__':
    main()

