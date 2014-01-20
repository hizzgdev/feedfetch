#! /usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import run,view,get 
import sqlite3
from docfetch import config_database
from html.parser import HTMLParser

html_parser = HTMLParser() 


_conn = sqlite3.connect(config_database)
_cursor = _conn.cursor()

page_size = 10

@get('/')
@get('/:page#\d*#')
@get('/:page#\d*#/')
@view('list')
def list_docs(page=1):
    offset = (int(page)-1)*page_size
    limit = page_size
    _cursor.execute('select count(*) from contents')
    rows = _cursor.fetchall()
    rowcount = rows[0][0]
    if rowcount % page_size > 0:
        pagecount = int(rowcount/page_size + 1)
    else:
        pagecount = int(rowcount/page_size)
        
    _cursor.execute('''select id,feed_name,entry_title,entry_time from contents
              order by entry_time desc limit ? offset ?
              ''',(limit,offset))
    rows = _cursor.fetchall()
    return dict(entries=rows,page=page,pagecount=pagecount,rowcount=rowcount)

@get('/doc/:id#\d*#')
@get('/doc/:id#\d*#/')
@view('detail')
def read_docs(id):
    _cursor.execute('''
    select id,feed_name,entry_title,entry_desc,entry_url,entry_time
    from contents where id=?''',(id,))
    rows = _cursor.fetchall()
    if len(rows) > 0:
        row = rows[0]
        #print(row[3])
        d=dict(
        id=row[0],
        feed=row[1],
        title=row[2],
        content=html_parser.unescape(row[3]),
        link=row[4],
        time=row[5])
    else:
        d=dict(
        id='',
        feed='',
        title='Not Found',
        content='',
        link='',
        time='')
    return d


if __name__ == '__main__':
    run()
