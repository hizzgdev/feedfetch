#! /usr/bin/env python2.7
# -*- coding:utf-8 -*-

from init     import init
from docfetch import fetch as fetch_doc
from imgfetch import fetch as fetch_img

if __name__ == '__main__':
    init()
    fetch_doc()
    fetch_img()
