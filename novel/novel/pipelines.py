# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter


class NovelPipeline:

    def __init__(self, host, db, port, user, password):
        self.host = host
        self.db = db
        self.port = port
        self.user = user
        self.password = password
        self.connect = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db,
                                       port=self.port, charset='utf8')
        self.cursor = self.connect.cursor()
        print('数据库连接成功 => %s' + '主机：', self.host + ' 端口：' + self.db)

    @classmethod
    def from_crawler(cls, crawler):
        db_name = crawler.settings.get('DB_SETTINGS')
        db_params = db_name.get('db1')
        return cls(
            host=db_params.get('host'),
            db=db_params.get('db'),
            user=db_params.get('user'),
            password=db_params.get('password'),
            port=db_params.get('port'),
        )

    def process_item(self, item, spider):
        table_fields = item.get('table_fields')
        table_name = item.get('table_name')
        if table_fields is None or table_name is None:
            raise Exception('必须要传表名table_name和字段名table_fields，表名或者字段名不能为空')
        values_params = '%s, ' * (len(table_fields) - 1) + '%s'
        keys = ', '.join(table_fields)
        values = ['%s' % str(item.get(i, '')) for i in table_fields]
        insert_sql = 'insert into %s (%s) values (%s);' % (table_name, keys, values_params)
        try:
            self.cursor.execute(insert_sql, tuple(values))
            print("数据插入成功 => " + '1')
        except Exception as e:
            print("执行sql异常 => " + str(e))
            pass
        finally:
            self.connect.commit()
        return item

    def close_spider(self, spider):
        self.connect.close()
        self.cursor.close()
