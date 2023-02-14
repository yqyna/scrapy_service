from itemadapter import ItemAdapter
import pymysql
from scrapy.exceptions import DropItem
from .items import *
import logging

logger = logging


class QswPipeline:

    def open_spider(self, spider):
        # 连接settings，MySQL字段
        data_config = spider.settings['DATA_CONFIG']
        # 判断数据库类型MySQL
        if data_config['type'] == 'mysql':
            self.conn = pymysql.connect(**data_config['config'])  # 建立连接
            self.cursor = self.conn.cursor()  # 游标
            spider.conn = self.conn
            spider.cursor = self.cursor

    # 存放数据
    def process_item(self, item, spider):
        print('*' * 50)
        # 判断管道
        if isinstance(item, QswItem):
            # 查找id在indo表中
            sql = 'select id from indo where title=%s and author=%s'
            # 执行sql语句
            self.cursor.execute(sql, (item['title'], item['author']))
            # 判断是否有id
            if self.cursor.fetchone():
                print('123456789')
            else:
                try:
                    # 添加字段
                    sql = 'insert into indo(title,author,hits,state,introd,url,c_time) VALUE (%s,%s,%s,%s,%s,%s,%s)'
                    self.cursor.execute(sql, (
                        item['title'],
                        item['author'],
                        item['hits'],
                        item['state'],
                        item['introd'],
                        item['url'],
                        item['c_time'],
                    ))
                    self.conn.commit()
                    # 章节信息写入
                    indo_id = self.cursor.lastrowid  # 关联外键
                    sql = 'insert into contents (indo_id,title,order1,c_time,url) VALUES '
                    for index, infos in enumerate(item['res_info']):
                        title, url = infos
                        print(title)
                        temp = '(%s,"%s",%s,"%s","%s"),' % (
                        indo_id, title.replace('"', ''), item['hits'], item['c_time'], url)
                        sql += temp  # sql语语句拼接
                    sql = sql[:-1]
                    try:
                        self.cursor.execute(sql)
                        self.conn.commit()
                    except Exception as e:
                        self.conn.rollback()
                        logger.warning('章节信息错误%s-%s' % (item['url'], e))
                except Exception as e:
                    self.conn.rollback()
                    logger.warning('信息写入错误%s-%s' % (item['url'], e))
        elif isinstance(item, Contentitem):
            print('-' * 50)
            sql = 'update contents set content=%s where id = %s'
            try:
                self.cursor.execute(sql, (item['content'], item['c_id']))
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()
                logger.warning('内容写入错误%s-%s' % (item['url'], e))
        else:
            print('0' * 50)
            raise DropItem

    def close_spider(self, spider):
        data_config = spider.settings['DATA_CONFIG']
        if data_config['type'] == 'mysql':
            self.conn.close()
            self.cursor.close()
