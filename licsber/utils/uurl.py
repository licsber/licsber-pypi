from collections import Counter
from urllib.parse import urlparse


def parse_host(url):
    parse = urlparse(url)
    host = parse.netloc
    return host


class UrlCache:
    """
    爬虫过程经常会碰到Connection Error,
    因此为了节省时间, 我们可以手动设定一个阈值,
    如果一个域名一直都请求超时, 就将此域名过滤.
    注意不适用于多进程情况.
    """

    def __init__(self, url_iterator, fail_threshold=50):
        self._cache = set()
        for url in url_iterator:
            self._cache.add(url)

        self.fail_host = Counter()
        self.fail_threshold = fail_threshold

    def check(self, url):
        host = parse_host(url)
        return self.fail_host[host] < self.fail_threshold

    def fail(self, url):
        host = parse_host(url)
        self.fail_host[host] += 1

    def _url_next(self):
        if len(self._cache):
            return self._cache.pop()
        else:
            raise StopIteration

    def __next__(self):
        url = self._url_next()
        while not self.check(url):
            url = self._url_next()
        else:
            return url

    def __iter__(self):
        return self
