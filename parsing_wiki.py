import requests
from bs4 import BeautifulSoup
import json

word = 'Калифорния'
url1 = f'https://ru.wikipedia.org/w/api.php?format=json&action=parse&page={word}&prop=text&section=77'
url1 = f'https://ru.wikipedia.org/w/api.php?format=json&action=parse&page={word}&prop=text'

data = json.loads(requests.get(url1).text, encoding='utf8')
print(data)
print(data['parse']['title'])
print(data['parse']['pageid'])
print(data['parse']['text']['*'])

# print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
# url = 'https://www.wikidata.org/w/api.php?action=wbgetentities&sites=ruwiki&titles=Калифорния&languages=ru&format=json'
# url = 'https://www.wikidata.org/w/api.php?action=wbavailablebadges&format=json' # ???
# data = json.loads(requests.get(url).text, encoding='utf8')
# print(data)