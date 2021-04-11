import base64

from pymongo import MongoClient
from pymongo.database import Database

from licsber.github import get_secret


class Mongo:
    def __init__(self, client, db_name, username, passwd):
        self.client = client
        self.db_name = db_name
        self.username = username
        self.passwd = passwd

    def connect(self) -> Database:
        db = self.client[self.db_name]
        db.authenticate(self.username, self.passwd)
        return db


def get_mongo(passwd_b64=get_secret('MONGO_PASSWD_B64'),
              host='mongodb://mongo.licsber.site',
              port=47107, db_name='auto', username='Automatic',
              connect=True):
    """
    获取mongo数据库连接, 用于爬虫.
    :param passwd_b64: base64后的密码.
    :param host: mongodb的url.
    :param port: host的端口.
    :param db_name: 数据库名称.
    :param username: 具有数据库权限的用户名.
    :param connect: 是否默认连接(选否会返回自定义对象 调用conn后才会认证).
    :return: mongo数据库连接.
    """
    if not passwd_b64:
        passwd_b64 = input('请输入mongo数据库连接密码(base64表示).')
    passwd = base64.b64decode(passwd_b64).decode('utf-8')
    c = MongoClient(host, port, connect=connect)
    if not connect:
        return Mongo(c, db_name, username, passwd)

    db = c[db_name]
    db.authenticate(username, passwd)
    return db
