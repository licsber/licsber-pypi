import hashlib
import os.path
import re

from bson import ObjectId
from minio import Minio

from licsber.mongo import idd_split_path


class S3Saver:
    def __init__(self, endpoint, access_key, secret_key, bucket_name, mongo_db):
        self.minio = Minio(endpoint, access_key, secret_key)
        self.bucket_name = bucket_name
        self.db = mongo_db
        self.db.create_index('suffix')
        self.re = re.compile(r'[a-z0-9]+/[a-z0-9]/[a-z0-9]/([a-z0-9]{24})\..*')

    def fput(self, filepath, save_md5=True, filename=False, dir_name=''):
        basename = os.path.basename(filepath)
        suffix = os.path.splitext(basename)[-1].strip('.')
        doc = {
            'suffix': suffix,
            'size': os.path.getsize(filepath),
        }
        if filename:
            doc['name'] = basename

        if dir_name:
            doc['dir'] = dir_name

        if save_md5:
            doc['md5'] = hashlib.md5(open(filepath, 'rb').read()).hexdigest()

        doc = self.db.insert_one(doc)
        idd = doc.inserted_id
        dst_path = idd_split_path(idd, suffix)
        self.minio.fput_object(self.bucket_name, dst_path, filepath)

    def del_file(self, idd, suffix):
        self.db.delete_one({'_id': ObjectId(idd)})
        self.minio.remove_object(self.bucket_name, idd_split_path(idd, suffix))

    def dedup(self):
        unique = set()
        for doc in self.db.find(projection=['suffix', 'md5', 'size']).sort([('_id', -1)]):
            if 'md5' not in doc:
                continue

            u = (doc['suffix'], doc['md5'], doc['size'])
            if u not in unique:
                unique.add(u)
            else:
                self.del_file(doc['_id'], doc['suffix'])

    def check_all(self):
        all_exist_idd = []
        for i in self.minio.list_objects(self.bucket_name, recursive=True):
            path = i.object_name
            if idd := self.re.fullmatch(path):
                idd = ObjectId(idd[1])
                all_exist_idd.append(idd)

        self.db.delete_many({
            '_id': {
                '$nin': all_exist_idd,
            }
        })
