#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import config
from app.lib.bottle import debug,run,TEMPLATE_PATH
from app.web.root import root

bind_host = config.app_host
bind_port = config.app_port
custom_tpl_path = config.tpl_path

if config.debug:
    debug(True)

if not custom_tpl_path:
    curr_path = os.path.split(os.path.realpath(__file__))[0]
    custom_tpl_path = curr_path+'/app/web/views/'
TEMPLATE_PATH.insert(0,custom_tpl_path)

run(app=root,host=bind_host,port=bind_port)
