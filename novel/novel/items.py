# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = scrapy.Field()
    table_fields = scrapy.Field()
    book = scrapy.Field()
    author = scrapy.Field()
    intro = scrapy.Field()
    detail_url = scrapy.Field()
    source = scrapy.Field()
    modify_time = scrapy.Field()
