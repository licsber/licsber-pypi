import hashlib
import os


class Meta:
    def __init__(self, filepath, buf_size=4 * 1024 * 1024):
        abspath = os.path.abspath(filepath)
        if not os.path.exists(abspath):
            print(f"文件不存在 请检查: {abspath}")
            exit(-1)

        self.buf_size = buf_size

        self._meta = {
            'abspath': abspath,
            'basename': os.path.basename(filepath),
            'size': os.path.getsize(filepath),
            'sha1': None,
            'md5': None,
            '115_sha1': None,
            'baidu_md5': None,
        }
        self._cal_all()

    @property
    def link_115(self):
        return f"115://{self.basename}|{self.size}|{self.sha1}|{self.head_sha1}"

    @property
    def link_ali(self):
        return f"aliyunpan://{self.basename}|{self.sha1}|{self.size}|TMP[Licsber]"

    @property
    def link_baidu(self):
        return f"{self.md5}#{self.head_md5}#{self.size}#{self.basename}"

    @property
    def csv_header(self):
        return 'Key,Filename,Size,SHA1,HeadSHA1,MD5,HeadMD5\n'

    def save_meta(self):
        with open(self.abspath + '.licsber.csv', 'w') as f:
            f.write(str(self))

    def __str__(self):
        res = self.csv_header
        res += f"Value,{self.basename},{self.size},{self.sha1},{self.head_sha1},{self.md5},{self.head_md5}\n"
        res += f",,,,,,{self.link_115}\n"
        res += f",,,,,,{self.link_ali}\n"
        res += f",,,,,,{self.link_baidu}"
        return res

    @property
    def abspath(self):
        return self._meta['abspath']

    @property
    def basename(self):
        return self._meta['basename']

    @property
    def size(self):
        return self._meta['size']

    @property
    def sha1(self):
        return self._meta['sha1']

    @property
    def md5(self):
        return self._meta['md5']

    @property
    def head_sha1(self):
        return self._meta['115_sha1']

    @property
    def head_md5(self):
        return self._meta['baidu_md5']

    def _cal_all(self):
        with open(self.abspath, 'rb') as f:
            head_sha1_obj = hashlib.sha1()
            num_bytes = 128 * 1024
            content = f.read(num_bytes)
            if (l := len(content)) < num_bytes:
                content += b'\0' * (num_bytes - l)
            head_sha1_obj.update(content)
            self._meta['115_sha1'] = head_sha1_obj.hexdigest().upper()

            f.seek(0)
            head_md5_obj = hashlib.md5()
            num_bytes = 256 * 1024
            content = f.read(num_bytes)
            if (l := len(content)) < num_bytes:
                content += b'\0' * (num_bytes - l)
            head_md5_obj.update(content)
            self._meta['baidu_md5'] = head_md5_obj.hexdigest().upper()

            f.seek(0)
            sha1_obj = hashlib.sha1()
            md5_obj = hashlib.md5()
            while True:
                content = f.read(self.buf_size)
                if not content:
                    break

                sha1_obj.update(content)
                md5_obj.update(content)

            self._meta['sha1'] = sha1_obj.hexdigest().upper()
            self._meta['md5'] = md5_obj.hexdigest().upper()


if __name__ == '__main__':
    test_path = '/tmp/test.licsber'
    with open(test_path, 'w') as f:
        f.write('Hello Licsber.')

    meta = Meta(test_path)
    meta.save_meta()
    print(meta, end='')
    assert meta.link_115 == '115://test.licsber|14|02B02681636CCEDB820385C8A87EA2E1E18ACD5C|C24486ADE0E6AAE9376E4994A7A1267277A13295'
