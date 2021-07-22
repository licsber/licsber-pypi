import os
from hashlib import sha1 as sha
from zlib import crc32 as crc


class Meta:
    def __init__(self, filepath):
        abs_path = os.path.abspath(filepath)
        self._p = abs_path
        self._c = None

        if not os.path.exists(abs_path):
            print(f"文件不存在 请检查: {abs_path}")
            exit(-1)

    def save_meta(self):
        with open(self._p + '.licsber.csv', 'w') as f:
            f.write(str(self))

    def size(self):
        return os.path.getsize(self._p)

    def content(self):
        if not self._c:
            self._c = open(self._p, 'rb').read()
        return self._c

    def sha1(self):
        sha1_obj = sha()
        content = self.content()
        sha1_obj.update(content)
        return sha1_obj.hexdigest()

    def crc32(self):
        content = self.content()
        return format(crc(content), 'x')

    def basename(self):
        return os.path.basename(self._p)

    def meta(self):
        basename = self.basename()
        size = self.size()
        sha1 = self.sha1()
        crc32 = self.crc32()
        return basename, size, sha1, crc32

    def __str__(self):
        res = 'Key,Filename,Size,SHA1,CRC32\n'
        basename, size, sha1, crc32 = self.meta()
        res += f"Value,{basename},{size},{sha1},{crc32}\n"
        return res


if __name__ == '__main__':
    test_path = '/tmp/test.licsber'
    with open(test_path, 'w') as f:
        f.write('Hello Licsber.')

    meta = Meta(test_path)
    meta.save_meta()
    print(meta)
