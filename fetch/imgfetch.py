#! /usr/bin/env python
# -*- coding:utf-8 -*-

import sqlite3
import uuid
#from urllib.request import urlopen
#from bs4 import BeautifulSoup
from urllib import urlopen
import BeautifulSoup
import config

class ImgFetch:
    def __init__(self):
        self.conn = sqlite3.connect(config.GenerateDB())

    def extract_url(self):
        pass

def download(feed_name,url,filename,extname=None):
    if feed_name.startswith('csdn'):
        true_url = url.split('?')[0]
    else:
        true_url = url
    try:
        resp = urlopen(true_url)
        data = resp.read(-1)
        resp.close()
        if extname == None:
            extname = get_extname(resp.getheader('Content-Type'))
        if extname == None:
            return
        fn = filename+extname
        f = open('images/'+fn,'wb')
        f.write(data)
        f.close()
        return fn
    except:
        print('download error:'+url);
        return None

def get_extname(content_type):
    print(content_type)
    if content_type=='image/jpeg':
        return '.jpg'
    elif content_type=='image/png':
        return '.png'
    elif content_type=='image/x-png':
        return '.png'
    elif content_type=='image/gif':
        return '.gif'
    elif content_type=='image/x-ms-bmp':
        return '.bmp'
    else:
        return None

def get_lasttime():
    _cursor.execute('select crtime from images order by crtime desc limit 1')
    rows = _cursor.fetchall()
    if len(rows)>0:
        return rows[0][0]
    else:
        return None

def run():
    #_cursor.execute('''drop table images''')
    #_cursor.execute('''create table images(
	#				id integer primary key,
	#				feed_name varchar(64),
	#				url nvarchar(512),
	#				filename nvarchar(64),
	#				crtime datetime)
    #''')
    #_cursor.execute('''create index images_url_index on images(url)
	#			''')
    #_conn.commit()
    
    last_time = get_lasttime()
    print(last_time)
    if last_time == None:
        sql = 'select feed_name,entry_desc,crtime from contents order by crtime'
    else:
        sql = 'select feed_name,entry_desc,crtime from contents where crtime > ? order by crtime'
    if last_time == None:
        _cursor.execute(sql)
    else:
        _cursor.execute(sql,(last_time,))
    rows = _cursor.fetchall()
    #print(rows)
    for row in rows:
        print(row[0])
        print(row[2])
        content = row[1]
        for img in BeautifulSoup(content).findAll('img'):
            #print(img)
            if 'src' in img.attrs:
                imgurl = img['src']
                #print(imgurl)
                if imgurl.startswith('http'):
                    _cursor.execute('select count(*) from images where url = ?',(imgurl,))
                    img_count = _cursor.fetchall()[0][0]
                    #print(img_count)
                    if img_count == 0 :
                        _cursor.execute('insert into images (feed_name,url,crtime) values (?,?,?)',(row[0],imgurl,row[2]))
        _conn.commit()
    _cursor.execute('''select id,feed_name,url from images where filename is null order by crtime''')
    rows = _cursor.fetchall()
    for row in rows:
        url = row[2]
        #print(url)
        filename = download(row[1],url,uuid.uuid1().hex)
        if filename != None:
            _cursor.execute('update images set filename = ? where id = ?',(filename,row[0]))
        else:
            _cursor.execute('update images set filename = ? where id = ?',('error',row[0]))
        _conn.commit()

    _conn.close()

if __name__ == '__main__':
    run()


