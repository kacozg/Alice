import os
from datetime import datetime
from hashlib import md5
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi

os.environ['TZ'] = 'America/Santiago'


class RequiredFieldsPipeline(object):
    """A pipeline to ensure the item have the required fields."""

    required_fields = ('url', 'title', 'picture', 'price', 'brand','tag1','tag2','tag3','tag4','tag5')

    def process_item(self, item, spider):
        for field in self.required_fields:
            if not item.get(field):
                raise DropItem("Field '%s' missing: %r" % (field, item))
        return item


class MySQLStorePipeline(object):
    """A pipeline to store the item in a MySQL database.
    This implementation uses Twisted's asynchronous database API.
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        id = self._get_id(item)
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')

        conn.execute("""SELECT EXISTS(
            SELECT 1 FROM products WHERE id = %s
        )""", (id, ))
        ret = conn.fetchone()[0]

        if ret:
            conn.execute("""
                UPDATE products
                SET url=%s, title=%s, picture=%s, price=%s, brand=%s, store=%s, id_store=%s, updated=%s, tag1=%s, tag2=%s, tag3=%s, tag4=%s, tag5=%s
                WHERE id=%s
            """, (item['url'], item['title'], item['picture'], item['price'], item['brand'], item['store'], item['id_store'], now, item['tag1'], item['tag2'] , item['tag3'], item['tag4'], item['tag5'], id))
            spider.log("Item updated in db: %s %r" % (id, item))
        else:
            conn.execute("""
                INSERT INTO products (id, url, title, picture, price, brand, store, id_store, updated, tag1, tag2, tag3, tag4, tag5)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (id, item['url'], item['title'], item['picture'], item['price'], item['brand'], item['store'], item['id_store'], now, item['tag1'], item['tag2'] , item['tag3'], item['tag4'], item['tag5']))
            spider.log("Item stored in db: %s %r" % (id, item))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        log.err(failure)

    def _get_id(self, item):
        # concat store with title and then generates the ID from that variable.
        idMd5 = item['store'] + item['title']
        idMd5 = idMd5.encode('utf-8')

        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(idMd5).hexdigest()
