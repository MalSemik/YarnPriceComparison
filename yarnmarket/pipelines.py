# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import MySQLdb
from scrapy.exceptions import NotConfigured
class DatabasePipeline(object):

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    def process_item(self, item, spider):
        return item

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:  # if we don't define db config in settings
            raise NotConfigured  # then reaise error
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        return cls(db, user, passwd, host)  # returning pipeline instance

    def open_spider(self, spider):
        self.conn = MySQLdb.connect(db=self.db,
                                    user=self.user, passwd=self.passwd,
                                    host=self.host,
                                    charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = "INSERT INTO table (name, url, page) VALUES (%s, %s, %s)"
        self.cursor.execute(sql,
                            (
                                item.get("name"),
                                item.get("url"),
                                item.get("page"),
                            )
                            )
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()
# class YarnmarketPipeline:
#     def process_item(self, item, spider):
#         return item
