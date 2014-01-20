#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
from time import mktime
from datetime import datetime
import feedparser
import sqlite3
from logger import fetch_logger as logger
import config

class DocFetch:
    def __init__(self):
        self.conn = sqlite3.connect(config.GenerateDB())
        logger.debug('open database')

    def __del__(self):
        self.conn.close()
        logger.debug('close database')

    def fetch(self):
        logger.info('start fetch document')
        for feed in config.feeds:
            self.fetch_feed(feed)
        logger.info('fetch task complete')


    def fetch_feed(self,feed):
        feed_name = feed['name']
        try:
            logger.info('start fetch feed \'%s\'', feed_name)
            fp = feedparser.parse(feed['url'])
            if len(fp.entries) > 0:
                feed['type'] = fp.version[0:3]
                logger.info('get %d articles from feed \'%s\'',len(fp.entries),feed_name)
                self.store(feed,fp.entries)
            else:
                logger.info('get nothing from feed \'%s\'',feed_name)
        except Exception as e:
            logger.error('get error while fetching feed \'%s\'',feed_name)
            logger.exception(e)
                        
    
    def store(self,feed,entries):
        feed_name = feed['name']
        feed_refresh_time = None
        if 'refresh' in feed.keys():
            feed_refresh_time = feed['refresh']
        if feed_refresh_time == None:
            feed_refresh_time = self.get_feed_refresh_time(feed_name)
        
        c = self.conn.cursor()
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

                logger.info('find new article \'%s\' from feed \'%s\'', entry.title,feed_name)
                if feed['type'] == 'ato':
                    self.save_doc(c,feed_name,entry.id,entry.title,entry.content[0].value,entry.link,entry_time)
                elif feed['type'] == 'rss':
                    self.save_doc(c,feed_name,entry.id,entry.title,entry.description,entry.link,entry_time)
                else:
                    pass

        feed['refresh'] = max_time

        self.conn.commit()
    
    def save_doc(self,cursor,feed_name,doc_id,doc_title,doc_content,doc_url,update_time):
        sql = 'select entry_time from contents where entry_url = ?'
        cursor.execute(sql,(doc_url,))
        rows = cursor.fetchall()
        if len(rows) > 0 :
            sql = 'delete from contents where entry_url = ?'
            cursor.execute(sql,(doc_url,))

        sql = 'insert into contents(feed_name,entry_id,entry_title,entry_desc,entry_url,entry_time) values(?,?,?,?,?,?)'
        params = (feed_name,doc_id,doc_title,doc_content,doc_url,update_time)
        cursor.execute(sql,params)
        logger.info('save new article \'%s\' to database', doc_title)
    
    def get_feed_refresh_time(self, feed_name):
        sql = 'select entry_time from contents where feed_name = ? order by entry_time desc limit 1'
        c = self.conn.cursor()
        c.execute(sql,(feed_name,))
        rows = c.fetchall()
        if len(rows) == 0:
            return None
        else:
            return datetime.strptime(rows[0][0],'%Y-%m-%d %H:%M:%S')


def fetch():
    df = DocFetch()
    df.fetch()

if __name__ == '__main__':
    fetch()


