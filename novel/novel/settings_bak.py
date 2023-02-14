# -*- coding:utf-8 -*-
# @FileName  :settings_bak.py
# @Time      :2023/2/14 15:57
# @Author    : yuhaiping
import pymysql

BOT_NAME = 'novel'

SPIDER_MODULES = ['novel.spiders']
NEWSPIDER_MODULE = 'novel.spiders'

ROBOTSTXT_OBEY = False

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
  'cookie': 'ASP.NET_SessionId=22da5okb1anxk5a3iezvbsuw; Hm_lvt_9007fab6814e892d3020a64454da5a55=1600827557,1601015578,1601015610,1601190738; codeyzgswso=e488b2230b94cd65; gsw2017user=1292023%7cE3869858693238EAC1DDA4FEC499C6DF; login=flase; wxopenid=defoaltid; gswZhanghao=18397716181; gswPhone=18397716181; Hm_lpvt_9007fab6814e892d3020a64454da5a55=1601190860',
}

DB_SETTINGS = {
    'db1': {
        'host': '127.0.0.1',
        'db': 'novel',
        'user': 'novel',
        'password': 'novel',
        'port': 3306,
        'cursorclass': pymysql.cursors.DictCursor,
    },
}
# 激活pipelines，需要添加才能够使用pipelines
ITEM_PIPELINES = {
   'novel.pipelines.NovelPipeline': 300,
}

FEED_EXPORT_ENCODING = 'utf-8'
