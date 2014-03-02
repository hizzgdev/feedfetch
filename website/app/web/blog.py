#! /usr/bin/env python
# -*- coding:utf-8 -*-

from app.lib.bottle import Bottle

blog = Bottle()

@blog.get('/')
def root_index():
	return 'blog'
