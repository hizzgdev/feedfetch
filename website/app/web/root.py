#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
from app.lib.bottle import Bottle,view,static_file

from app.web.blog import blog
from app.web.bbs import bbs

root = Bottle()

root.mount(blog,'/blog')
root.mount(bbs,'/bbs')


curr_path = os.path.split(os.path.realpath(__file__))[0]
static_path = curr_path+'/static'

@root.get('/')
@view('index')
def root_index():
	return dict(title='root')

@root.get('/static/:path#.*#')
def static_route(path):
    return static_file(path,root=static_path)

