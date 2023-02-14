# -*- coding:utf-8 -*-
# @FileName  :novel_spider.py
# @Time      :2023/2/14 15:47
# @Author    : yuhaiping
import datetime

import scrapy

from novel.items import NovelItem

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36'
}


class NovelSpider(scrapy.Spider):

    name = "novel"

    start_urls = ['http://books.phoenixfm.cn/']
    table_name = 'app_user_book_manage'
    table_fields = ['book', 'author', 'intro', 'detail_url', 'source', 'modify_time']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        book_info_divs = response.xpath('//*[@class="items_txt"]')

        for book_info in book_info_divs:
            item = NovelItem()
            item['table_name'] = self.table_name
            item['table_fields'] = self.table_fields
            current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['modify_time'] = current_date
            item['book'] = book_info.xpath('./h4/a/text()').get()
            item['author'] = book_info.xpath('./p[@class="author"]/a/text()').get()
            item['intro'] = book_info.xpath('./p[@class="intro"]/a/text()').get()
            item['detail_url'] = book_info.xpath('./p[@class="intro"]/a/@href').get()
            item['source'] = self.start_urls[0]
            yield item
