#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import logging
import logging.config

if not os.path.isdir('logs'):
    os.mkdir('logs')

logging.config.fileConfig('logger.conf')
fetch_logger = logging.getLogger('fetch')

"""
fetch_formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
fetch_handler_file = logging.FileHandler('fetch.log')
fetch_handler_file.setFormatter(fetch_formatter)
fetch_handler_console = logging.StreamHandler()
fetch_handler_console.setFormatter(fetch_formatter)
fetch_logger = logging.getLogger('fetch')
fetch_logger.setLevel(logging.INFO)
fetch_logger.addHandler(fetch_handler_file)
fetch_logger.addHandler(fetch_handler_console)
"""

"""
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='fetch.log',
    filemode='a'
)
"""

if __name__ == '__main__':
    fetch_logger.info('info')
