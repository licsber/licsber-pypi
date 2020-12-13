import requests
import urllib3
from requests import Session
from requests.adapters import HTTPAdapter


def get_session(retry_time=3) -> Session:
    urllib3.disable_warnings()
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=retry_time))
    s.mount('https://', HTTPAdapter(max_retries=retry_time))
    return s
