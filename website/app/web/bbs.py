#! /usr/bin/env python
# -*- coding:utf-8 -*-

from app.lib.bottle import Bottle

bbs = Bottle()

@bbs.get('/')
def root_index():
	return 'bbs'
