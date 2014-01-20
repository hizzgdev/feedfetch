#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
from time import mktime
from datetime import datetime
import feedparser
import sqlite3
import logging
import imagefetch
from config import config_feeds,config_database
#from config_debug import config_feeds,config_database

class docfetch:
    def __init__(self):
        self.initialized = os.path.isfile(config_database)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename='docfetch.log',
            filemode='a'
        )
    
    def run(self):
        logging.info('start fetch document')
        for feed in config_feeds:
            self.fetch(feed)
        logging.info('start fetch image')
        imagefetch.run();
        logging.info('fetch task complete')
    
    def fetch(self,feed):
        try:
            print('start fetch feed:'+feed['name'])
            logging.info('start fetch feed:'+feed['name'])
            fp = feedparser.parse(feed['url'])
            if len(fp.entries) > 0:
                feed['type'] = fp.version[0:3]
                logging.info('get '+str(len(fp.entries))+ ' articles ')
                self.store(feed,fp.entries)
            else:
                logging.info('get empty entries')
        except Exception as e:
            logging.info('start fetch feed:'+feed['name']+' error')
            logging.error(e)
                        
    
    def store(self,feed,entries):
        feed_name = feed['name']
        feed_refresh_time = None
        if 'refresh' in feed.keys():
            feed_refresh_time = feed['refresh']
        if feed_refresh_time == None:
            feed_refresh_time = self.get_feed_refresh_time(feed_name)

        conn = self.get_conn()
        c = conn.cursor()
        for entry in entries:
            if feed['type'] == 'ato':
                entry_time = datetime.fromtimestamp(mktime(entry.updated_parsed))
            elif feed['type'] == 'rss':
                entry_time = datetime.fromtimestamp(mktime(entry.published_parsed))
            else:
                pass

            max_time = None
            if feed_refresh_time == None or entry_time > feed_refresh_time:
                if max_time == None or max_time < entry_time:
                    max_time = entry_time

                logging.info('save new article :'+entry.title)
                if feed['type'] == 'ato':
                    self.save_doc(c,feed_name,entry.id,entry.title,entry.content[0].value,entry.link,entry_time)
                elif feed['type'] == 'rss':
                    self.save_doc(c,feed_name,entry.id,entry.title,entry.description,entry.link,entry_time)
                else:
                    pass

        feed['refresh'] = max_time

        conn.commit()
        conn.close()
    
    def get_conn(self):
        conn = sqlite3.connect(config_database)
        if not self.initialized:
            self.initialized = True
            cursor = conn.cursor()
            cursor.execute('''
                create table contents(
                    id integer primary key,
                    feed_name varchar(64),
                    entry_id varchar(64),
                    entry_title varchar(128),
                    entry_desc text,
                    entry_url varchar(128) unique,
                    entry_time datetime,
                    crtime datetime default (datetime('now','localtime'))
                )
                ''')
            cursor.execute('''
                create index contents_feed_name_index on contents(feed_name)
                ''')
            cursor.execute('''
                create index contents_entry_url_index on contents(entry_url)
                ''')
            cursor.execute('''
                create index contents_entry_time_index on contents(entry_time)
                ''')
            _cursor.execute('''
                create table images(
                    id integer primary key,
                    feed_name varchar(64),
                    url nvarchar(512),
                    filename nvarchar(64),
                    crtime datetime
                )''')
            _cursor.execute('''
                create index images_url_index on images(url)
                ''')
            conn.commit()
        return conn

    def save_doc(self,cursor,feed_name,doc_id,doc_title,doc_content,doc_url,update_time):
        sql = 'select entry_time from contents where entry_url = ?'
        cursor.execute(sql,(doc_url,))
        rows = cursor.fetchall()
        if len(rows) > 0 :
            sql = 'delete from contents where entry_url = ?'
            cursor.execute(sql,(doc_url,))

        sql = 'insert into contents(feed_name,entry_id,entry_title,entry_desc,entry_url,entry_time) values(?,?,?,?,?,?)'
        params = (feed_name,doc_id,doc_title,doc_content,doc_url,update_time)
        #print(doc_title)
        #print(update_time)
        cursor.execute(sql,params)
    
    def get_feed_refresh_time(self, feed_name):
        sql = 'select entry_time from contents where feed_name = ? order by entry_time desc limit 1'
        conn = self.get_conn()
        c = conn.cursor()
        c.execute(sql,(feed_name,))
        rows = c.fetchall()
        if len(rows) == 0:
            return None
        else:
            return datetime.strptime(rows[0][0],'%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    print('正在抓取技术文章，请不要关闭，抓取结束后会自动关闭。谢谢理解。')
    df = docfetch()
    df.run()


