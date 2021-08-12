import hashlib
import os.path
import re

from bson import ObjectId
from minio import Minio

from licsber.mongo import idd_split_path


class S3Saver:
    def __init__(self, endpoint, access_key, secret_key, bucket_name, mongo_db):
        self.minio = Minio(endpoint, access_key, secret_key)
        if not self.minio.bucket_exists(bucket_name):
            self.minio.make_bucket(bucket_name)

        self.bucket_name = bucket_name
        self.db = mongo_db
        self.db.create_index('suffix')
        self.re = re.compile(r'[a-z0-9]+/[a-z0-9]/[a-z0-9]/([a-z0-9]{24})\..*')

    def fput(self, filepath, save_md5=True, filename=False, dir_name='', custom_dict=None):
        """
        保存文件到minio.
        保存元信息到mongo.
        :param filepath: 文件路径.
        :param save_md5: 是否保存md5.
        :param filename: 是否保存原始文件名.
        :param dir_name: 自定义文件夹分类名.
        :param custom_dict: 自定义字段字典.
        :return: 
        """
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

        if custom_dict:
            doc.update(custom_dict)

        doc = self.db.insert_one(doc)
        idd = doc.inserted_id
        dst_path = idd_split_path(idd, suffix)
        self.minio.fput_object(self.bucket_name, dst_path, filepath)

    def del_file(self, idd, suffix):
        self.db.delete_one({'_id': ObjectId(idd)})
        self.minio.remove_object(self.bucket_name, idd_split_path(idd, suffix))

    def dedup(self):
        """
        清除数据库和minio中md5、size都相同的文件.
        :return:
        """
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
        """
        用minio中的所有文件更新数据库.
        :return:
        """
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
