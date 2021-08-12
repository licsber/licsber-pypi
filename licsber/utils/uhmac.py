import base64
import datetime
import hashlib
import hmac

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


def get_tencent_sign(source, secret_id, secret_key):
    date_time = datetime.datetime.utcnow().strftime(GMT_FORMAT)
    auth = f'hmac id="{secret_id}", algorithm="hmac-sha1", headers="date source", signature="'
    sign_str = f"date: {date_time}\nsource: {source}"
    sign_str = hmac.new(secret_key.encode(), sign_str.encode(), hashlib.sha1).digest()
    sign_str = base64.b64encode(sign_str).decode()
    sign_str = auth + sign_str + '"'
    return sign_str, date_time


def get_tencent_headers(source, secret_id, secret_key):
    sign_str, date_time = get_tencent_sign(source, secret_id, secret_key)
    return {
        'Source': source,
        'Authorization': sign_str,
        'Date': date_time,
    }
