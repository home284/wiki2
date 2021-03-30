import requests
import json

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 YaBrowser/21.2.4.165 Yowser/2.5 Safari/537.36',
}
url = 'https://ru.wikipedia.org/w/rest.php/v1/page/Готы'
data = json.loads(requests.get(url, headers=headers).text)
print(data)