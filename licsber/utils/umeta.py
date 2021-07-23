import hashlib
import os
import zlib


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
        sha1_obj = hashlib.sha1()
        content = self.content()
        sha1_obj.update(content)
        return sha1_obj.hexdigest()

    def crc32(self):
        content = self.content()
        return format(zlib.crc32(content), 'x')

    def basename(self):
        return os.path.basename(self._p)

    def gen_115_link(self):
        basename = self.basename()
        size = self.size()
        sha1 = self.sha1().upper()
        with open(self._p, 'rb') as f:
            sha1_obj = hashlib.sha1()
            num_bytes = 128 * 1024
            content = f.read(num_bytes)
            if (l := len(content)) < num_bytes:
                content += b'\0' * (num_bytes - l)

            sha1_obj.update(content)
            head_sha1 = sha1_obj.hexdigest().upper()

        return f"115://{basename}|{size}|{sha1}|{head_sha1}"

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
    assert meta.gen_115_link() == '115://test.licsber|14|02B02681636CCEDB820385C8A87EA2E1E18ACD5C|C24486ADE0E6AAE9376E4994A7A1267277A13295'
