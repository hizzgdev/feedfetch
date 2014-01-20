#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sqlite3
from config import GenerateDB

init_sqls = [
    '''create table contents(
        id integer primary key,
        feed_name varchar(64),
        entry_id varchar(64),
        entry_title varchar(128),
        entry_desc text,
        entry_url varchar(128) unique,
        entry_time datetime,
        crtime datetime default (datetime('now','localtime'))
    )''',
    '''create index contents_feed_name_index on contents(feed_name)''',
    '''create index contents_entry_url_index on contents(entry_url)''',
    '''create index contents_entry_time_index on contents(entry_time)''',
    '''create table images(
        id integer primary key,
        feed_name varchar(64),
        url nvarchar(512),
        filename nvarchar(64),
        crtime datetime
    )''',
    '''create index images_url_index on images(url)'''
]
def init_db():
    db = GenerateDB()
    if not os.path.isfile(db):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        for sql in init_sqls:
            cursor.execute(sql)
        conn.commit()
        conn.close()

def init():
    init_db()

