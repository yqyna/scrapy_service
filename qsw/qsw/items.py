# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QswItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    hits = scrapy.Field()
    state = scrapy.Field()
    introd = scrapy.Field()
    url = scrapy.Field()
    res_info = scrapy.Field()
    c_time = scrapy.Field()


# 小说内容存储管道
class Contentitem(scrapy.Item):
    content = scrapy.Field()
    c_id = scrapy.Field()
    c_url = scrapy.Field()
