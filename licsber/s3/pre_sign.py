from datetime import timedelta

import minio


class S3Sign:
    def __init__(self, url, access_key, secret_key, region=''):
        self.url = url
        self.region = region
        self.cred = minio.api.StaticProvider(access_key, secret_key).retrieve()

    def get(self, bucket, path, expires=timedelta(minutes=5)):
        url = minio.api.BaseURL(self.url, self.region).build(
            method='GET',
            region=self.region,
            bucket_name=bucket,
            object_name=path,
        )

        url = minio.api.presign_v4(
            method='GET',
            url=url,
            region=self.region,
            credentials=self.cred,
            date=minio.api.time.utcnow(),
            expires=int(expires.total_seconds()),
        )
        return minio.api.urlunsplit(url)
