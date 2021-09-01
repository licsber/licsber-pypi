from datetime import timedelta

import minio
import urllib3

urllib3.disable_warnings()

from licsber.github import get_secret


def get_s3(
        endpoint=get_secret('L_S3_ENDPOINT'),
        access_key=get_secret('L_S3_ACCESS'),
        secret_key=get_secret('L_S3_SECRET'),
        verify=False,
        **kwargs,
):
    http_client = None
    if not verify:
        timeout = timedelta(minutes=5).seconds
        http_client = urllib3.PoolManager(
            timeout=urllib3.util.Timeout(connect=timeout, read=timeout),
            maxsize=10,
            cert_reqs='CERT_NONE',
            retries=urllib3.Retry(
                total=5,
                backoff_factor=0.2,
                status_forcelist=[500, 502, 503, 504]
            )
        )

    s3 = minio.Minio(
        endpoint=endpoint,
        access_key=access_key,
        secret_key=secret_key,
        http_client=http_client,
        **kwargs,
    )

    return s3
