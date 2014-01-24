#! /usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sqlite3
import uuid
import urllib2
#from urllib.request import urlopen
#from bs4 import BeautifulSoup
#from urllib import urlopen
from BeautifulSoup import BeautifulSoup
from urlparse import urljoin
from logger import fetch_logger as logger

import config

USER_AGENT          = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.76 Safari/537.36'
DOWNLOAD_TIMEOUT    = 30

STATE_SUCCESS       = 1
STATE_BADURL        = 2
STATE_NETWORK_ERROR = 4

class ImgFetch:
    def __init__(self):
        self.conn = sqlite3.connect(config.GenerateDB())
        self.image_dir = config.GenerateImageDir()
        logger.debug('open database at ImgFetch')

    def __del__(self):
        self.conn.close()
        logger.debug('close database at ImgFetch')

    def fetch(self):
        logger.info('start fetch images')
        self.extract_url()
        self.check_images()
        logger.info('images fetch complete')

    def extract_url(self):
        logger.info('start search images from document')
        cursor = self.conn.cursor()
        sql = 'select id, feed_name, entry_url, entry_desc from contents where state&1 = 0'
        cursor.execute(sql)
        rows = cursor.fetchall()
        logger.info('get %d new documents', len(rows))
        for row in rows:
            id = row[0]
            feed = row[1]
            docurl = row[2]
            content = row[3]
            logger.info('extract image from doc \'%s\'',docurl)
            for img in BeautifulSoup(content).findAll('img'):
                if img.has_key('src'):
                    imgurl = img['src']
                    logger.info('find image \'%s\'',imgurl)
                    if not imgurl.startswith('http'):
                        imgurl = urljoin(docurl,imgurl)
                    logger.info('image\'s full url is \'%s\'',imgurl)

                    cursor.execute('select count(*) from images where url = ?',(imgurl,))
                    img_count = cursor.fetchall()[0][0]
                    if img_count == 0:
                        logger.info('it is a new image')
                        cursor.execute('insert into images (feed_name,url,state) values (?,?,0)',(feed,imgurl))
                        logger.info('insert this image url to database')
                    else:
                        logger.info('this image is already exists')
            cursor.execute('update contents set state = state|1 where id = ?',(id,))
            self.conn.commit()

    def check_images(self):
        cursor = self.conn.cursor()

        # new images
        logger.info('start list all new images for download')
        sql = 'select id, feed_name, url from images where state = 0'
        cursor.execute(sql)
        rows = cursor.fetchall()
        self.download_images(rows,cursor)

        # recent error images
        logger.info('start list recent error images for download')
        sql = 'select id, feed_name, url from images where state&? = ? and crtime > datetime(\'now\',\'-24 hour\')'
        cursor.execute(sql,(STATE_SUCCESS,0))
        rows = cursor.fetchall()
        self.download_images(rows,cursor)

        cursor.close()
        self.conn.commit()

    def download_images(self,rows,cursor):
        for row in rows:
            imgid = row[0]
            feed = row[1]
            url = row[2]
            logger.info('prepare download image#%d \'%s\'',imgid,url)
            (filename,state,message) = self.download(feed,url,uuid.uuid1().hex)
            if filename != None:
                logger.info('download image success, local filename is \'%s\'',filename)
                cursor.execute('update images set filename = ?, state = state|? where id = ?',(filename,state,imgid))
            else:
                logger.info('download image fail: %s',message)
                cursor.execute('update images set state = state|? where id = ?',(state,imgid))
            self.conn.commit()

    def download(self,feed,url,filename,extname=None):
        if feed.startswith('csdn'):
            true_url = url.split('?')[0]
        else:
            true_url = url
        logger.info('downloading image \'%s\'',url)
        try:
            req = urllib2.Request(true_url)
            req.add_header('User-Agent',USER_AGENT)
            resp = urllib2.urlopen(req,None,DOWNLOAD_TIMEOUT)
            #resp = urlopen(true_url)
            #logger.debug(resp.getcode())
            data = resp.read(-1)
            resp.close()
            if extname == None:
                #in python3
                #content_type = resp.getheader('Content-Type')
                #in python2
                content_type = resp.info().getheader('Content-Type').lower()
                extname = self.get_extname(content_type)
            if extname == None:
                logger.warning('unsupported content type \'%s\'',content_type)
                return (None, STATE_BADURL, 'unsupported content type \''+content_type+'\'')
            file_fullname = filename+extname
            fn = os.path.join(self.image_dir,os.path.join(file_fullname[:1],os.path.join(file_fullname[1:2],file_fullname)))
            f = open(fn,'wb')
            f.write(data)
            f.close()
            return (file_fullname, STATE_SUCCESS, 'success')
        except Exception as e:
            logger.error('an error accur while downloading %s',url);
            logger.exception(e)
            return (None, STATE_NETWORK_ERROR, 'network error')

    def get_extname(self,content_type):
        if content_type.startswith('image/jpeg'):
            return '.jpg'
        elif content_type.startswith('image/pjpeg'):
            return '.jpg'
        elif content_type.startswith('image/png'):
            return '.png'
        elif content_type.startswith('image/x-png'):
            return '.png'
        elif content_type.startswith('image/gif'):
            return '.gif'
        elif content_type.startswith('image/x-ms-bmp'):
            return '.bmp'
        else:
            return None


def fetch():
    imgFetch = ImgFetch()
    imgFetch.fetch()

if __name__ == '__main__':
    fetch()


