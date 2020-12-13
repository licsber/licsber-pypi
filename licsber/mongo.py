import base64

from pymongo import MongoClient
from pymongo.database import Database

from .github import get_secret


def get_mongo(passwd_b64=get_secret('MONGO_PASSWD_B64'),
              host='mongodb://mongo.licsber.site',
              port=47107, db_name='auto', username='Automatic'
              ) -> Database:
    """
    获取mongo数据库连接, 用于爬虫.
    :param passwd_b64: base64后的密码.
    :param host: mongodb的url.
    :param port: host的端口.
    :param db_name: 数据库名称.
    :param username: 具有数据库权限的用户名.
    :return: mongo数据库连接.
    """
    if not passwd_b64:
        passwd_b64 = input('请输入mongo数据库连接密码(base64表示).')
    c = MongoClient(host, port)
    db = c[db_name]
    db.authenticate(username, base64.b64decode(passwd_b64).decode('utf-8'))
    return db
