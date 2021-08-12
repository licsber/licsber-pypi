from datetime import timedelta
from threading import Lock

from bson import ObjectId

from licsber.mongo import random_get, idd_split_path
from .pre_sign import S3Sign


class LinkGen:
    def __init__(self,
                 endpoint,
                 access_key,
                 secret_key,
                 bucket_name,
                 mongo_db,
                 match_dict=None,
                 pre_fetch_num=2048,
                 expire_minute=5):
        if not match_dict:
            match_dict = {}

        self.bucket_name = bucket_name
        self.db = mongo_db
        self.match_dict = match_dict
        self.pre_fetch_num = pre_fetch_num
        self.expire_minute = expire_minute

        self.lock = Lock()
        self.cache = self._request_db()
        self.sign = S3Sign(endpoint, access_key, secret_key)

    def _request_db(self):
        return random_get(self.db,
                          match=self.match_dict,
                          size=self.pre_fetch_num,
                          project={'suffix': True},
                          )

    def _gen_link(self, idd, suffix):
        path = idd_split_path(idd, suffix)
        return self.sign.get(
            self.bucket_name, path, timedelta(minutes=self.expire_minute)
        )

    def random_get(self):
        if not self.cache:
            self.lock.acquire()
            if not self.cache:
                self.cache = self._request_db()

            self.lock.release()

        item = self.cache.pop()
        return self._gen_link(item['_id'], item['suffix'])

    def gen_link_by_idd(self, idd):
        doc = self.db.find_one({
            '_id': ObjectId(idd),
        }, projection=['suffix'])
        return self._gen_link(doc['_id'], doc['suffix'])
