#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
from datetime import date

CONTENT_DIR = 'contents'

def GenerateDB():
    month_dir = GenerateMonthlyDir()
    return os.path.join(month_dir,'doc.db')

def GenerateImageDir():
    month_dir = GenerateMonthlyDir()
    dir = os.path.join(month_dir,'images')
    if not os.path.isdir(dir):
        os.mkdir(dir)
        for s in '0123456789abcdef':
            subdir = os.path.join(dir,s)
            os.mkdir(subdir)
            for s1 in '0123456789abcdef':
                os.mkdir(os.path.join(subdir,s1))
    return dir

def GenerateMonthlyDir():
    MonthStr = date.today().strftime('%Y%m')
    p = os.path.join(CONTENT_DIR,MonthStr)
    if not os.path.isdir(p):
        os.makedirs(p)
    return p

feeds=[
    {
        'name':'iteye',
        'url':'http://www.iteye.com/rss/blogs'
    },
    {
        'name':'iteye_web',
        'url':'http://www.iteye.com/rss/blogs/category/web'
    #,'x':"""
    },
    {
        'name':'iteye_arch',
        'url':'http://www.iteye.com/rss/blogs/category/architecture'
    },
    {
        'name':'iteye_language',
        'url':'http://www.iteye.com/rss/blogs/category/language'
    },
    {
        'name':'iteye_internet',
        'url':'http://www.iteye.com/rss/blogs/category/internet'
    },
    {
        'name':'iteye_os',
        'url':'http://www.iteye.com/rss/blogs/category/os'
    },
    {
        'name':'iteye_db',
        'url':'http://www.iteye.com/rss/blogs/category/database'
    },
    {
        'name':'iteye_develop',
        'url':'http://www.iteye.com/rss/blogs/category/develop'
    },
    {
        'name':'iteye_industry',
        'url':'http://www.iteye.com/rss/blogs/category/industry'
    },
    {
        'name':'csdn_web',
        'url':'http://blog.csdn.net/rss.html?type=Home&channel=web'
    },
    {
        'name':'csdn_enterprise',
        'url':'http://blog.csdn.net/rss.html?type=Home&channel=enterprise'
    },
    {
        'name':'csdn_code',
        'url':'http://blog.csdn.net/rss.html?type=Home&channel=code'
    },
    {
        'name':'csdn_database',
        'url':'http://blog.csdn.net/rss.html?type=Home&channel=database'
    },
    {
        'name':'csdn_system',
        'url':'http://blog.csdn.net/rss.html?type=Home&channel=system'
    },
    {
        'name':'csdn_software',
        'url':'http://blog.csdn.net/rss.html?type=Home&channel=software'
    #"""
    }
]


