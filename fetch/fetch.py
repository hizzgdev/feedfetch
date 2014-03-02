#! /usr/bin/env python2.7
# -*- coding:utf-8 -*-

import time
from init     import init
from docfetch import fetch as fetch_doc
from imgfetch import fetch as fetch_img

def run():
    init()
    fetch_doc()
    fetch_img()

def debug(sn):
    print(sn)

def runAsService():
    serialNo = 0
    while True:
        serialNo = serialNo + 1
        if serialNo == 10:
            break
        debug(serialNo)
        time.sleep(1)


if __name__ == '__main__':
    try:
        runAsService()
    except KeyboardInterrupt as e:
        debug(999)
        print('bye bye')
