import requests
import json
from datetime import date, timedelta

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 YaBrowser/21.2.4.165 Yowser/2.5 Safari/537.36',
}

def get_pageviews_by_days(code, delta=timedelta(days=62)):
    """ period can be month/day/ """
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/ru.wikipedia/all-access/all-agents/{code}/monthly/{(date.today()-delta).strftime('%Y%m%d')}/{date.today().strftime('%Y%m%d')}"
    data = json.loads(requests.get(url, headers=headers).text)
    return data

code = 'Готы'
data = get_pageviews_by_days(code)
for item in data['items']:
    print(item)