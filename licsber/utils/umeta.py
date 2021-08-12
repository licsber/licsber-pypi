import hashlib
import os


class Meta:
    def __init__(self, filepath, buf_size=4 * 1024 * 1024):
        abs_path = os.path.abspath(filepath)
        if not os.path.exists(abs_path):
            print(f"文件不存在 请检查: {abs_path}")
            exit(-1)

        self.buf_size = buf_size

        self._path = abs_path
        self._basename = os.path.basename(filepath)
        self._size = os.path.getsize(filepath)
        self._sha1 = None
        self._md5 = None
        self._115_head_hash = None
        self._baidu_head_hash = None

    def gen_115_link(self):
        sha1, _ = self.get_sha1_and_md5()
        head_sha1 = self.get_115_head_hash()
        return f"115://{self._basename}|{self._size}|{sha1}|{head_sha1}"

    def gen_ali_link(self):
        sha1, _ = self.get_sha1_and_md5()
        return f"aliyunpan://{self._basename}|{sha1}|{self._size}|TMP"

    def save_meta(self):
        with open(self._path + '.licsber.csv', 'w') as f:
            f.write(str(self))

    def get_basename(self):
        return self._basename

    def get_size(self):
        return self._size

    def get_sha1_and_md5(self):
        def cal():
            sha1_obj = hashlib.sha1()
            md5_obj = hashlib.md5()
            with open(self._path, 'rb') as f:
                while True:
                    content = f.read(self.buf_size)
                    if not content:
                        break

                    sha1_obj.update(content)
                    md5_obj.update(content)

            self._sha1 = sha1_obj.hexdigest().upper()
            self._md5 = md5_obj.hexdigest().upper()

        if not self._sha1 or not self._md5:
            cal()

        return self._sha1, self._md5

    def get_115_head_hash(self):
        def cal():
            with open(self._path, 'rb') as f:
                sha1_obj = hashlib.sha1()
                num_bytes = 128 * 1024
                content = f.read(num_bytes)
                if (l := len(content)) < num_bytes:
                    content += b'\0' * (num_bytes - l)

                sha1_obj.update(content)
                self._115_head_hash = sha1_obj.hexdigest().upper()

        if not self._115_head_hash:
            cal()

        return self._115_head_hash

    def get_baidu_head_hash(self):
        raise Exception('暂时还没做')

    def meta(self):
        self.gen_115_link()
        return self._basename, self._size, self._sha1, self._115_head_hash, self._md5

    def __str__(self):
        res = 'Key,Filename,Size,SHA1,HeadSHA1,MD5\n'
        sha1, md5 = self.get_sha1_and_md5()
        head_sha1 = self.get_115_head_hash()
        res += f"Value,{self._basename},{self._size},{sha1},{head_sha1},{md5}\n"
        res += f",,,,,{self.gen_115_link()}\n"
        res += f",,,,,{self.gen_ali_link()}\n"
        return res


if __name__ == '__main__':
    test_path = '/tmp/test.licsber'
    with open(test_path, 'w') as f:
        f.write('Hello Licsber.')

    meta = Meta(test_path)
    meta.save_meta()
    print(meta, end='')
    assert meta.gen_115_link() == '115://test.licsber|14|02B02681636CCEDB820385C8A87EA2E1E18ACD5C|C24486ADE0E6AAE9376E4994A7A1267277A13295'
