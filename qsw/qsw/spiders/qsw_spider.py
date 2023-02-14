# -*- coding:utf-8 -*-
# @FileName  :qsw_spider.py
# @Time      :2023/2/14 16:44
# @Author    : yuhaiping

import scrapy
from ..items import QswItem, Contentitem
from datetime import datetime
class XsSpider(scrapy.Spider):
    name = 'xs'
    allowed_domains = ['quanshu.92kaifa.com']
    #初始url
    start_urls = ['http://quanshu.92kaifa.com/list/2_0.html']
    #提取所有书籍的url
    def parse(self, response):
        url=response.xpath('//ul[@class="seeWell cf"]/li/a/@href').extract()
        # print(url)
        # url1=s_url+str(url)
        d_url = 'http://quanshu.92kaifa.com'
        for u in url[:1]:#这里只爬了一个url
            d_u  = d_url+u
            # 对书籍url进行请求
            yield scrapy.Request(url=d_u,callback=self.parse_connet)
    #请求书籍页，提取相关数据
    def parse_connet(self,response):
        item = QswItem()
        item['title'] =response.xpath('//div[@class="detail"]/div/h1/text()').extract_first()
        item['author'] =response.xpath('//div[@class="bookDetail"]/dl[3]/dd/a/text()').extract_first()
        item['hits'] =response.xpath('//div[@class="bookDetail"]/dl[2]/dd/text()').extract_first()
        item['state'] =response.xpath('//div[@class="bookDetail"]/dl[1]/dd/text()').extract_first()
        item['introd'] =response.xpath('//div[@id="waa"]/text()').extract_first()
        item['url'] =response.url
        item['c_time'] = datetime.now()
        # print(item)
        #对章节所在页的url进行请求
        e_url = 'http://quanshu.92kaifa.com'
        zj_url = e_url+response.xpath('//div[@class="b-oper"]/a[1]/@href').extract_first()
        return scrapy.Request(url=zj_url,callback=self.parse_info,meta={'info':item})
    #提取章节信息
    def parse_info(self,response):
        r_url = 'http://quanshu.92kaifa.com'
        info = response.meta.get('info')
        zjinfo = response.xpath('//div[@class="clearfix dirconone"]/li/a')
        infos = [(a.xpath('./text()').extract_first(),(r_url+a.xpath('./@href').extract_first()))for a in zjinfo]
        info['res_info'] = infos
        # print ( info )
        yield info
        #小说内容
        sql = 'select id,url from contents where content is NULL '  #结果为元组
        self.cursor.execute(sql)
        for i in self.cursor.fetchall():
            # 对章节url进行请求
            yield scrapy.Request(i[1],callback=self.parse_content_info,meta={'id':i[0]})
#提取详细内容
    def parse_content_info(self,response):
        item = Contentitem()
        print('一'*50)
        item['content'] = ''.join(response.xpath('//div[@id="content"]/text()').extract()).strip()
        item['c_id'] = response.meta['id']
        item['c_url'] = response.url