import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

def parse_cats(code):
    result = []
    url = f'https://ru.wikipedia.org{code}'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    # Сначала парсим конечные страницы
    div = soup.find('div', {'id': 'mw-pages'})
    if div:
        for li in div.findAll('li'):
            cat = {}
            cat['title'] = li.a.text.strip()
            cat['href'] = unquote(li.a['href'].strip())
            cat['type'] = 'page'
            result.append(cat)
    # Теперь смотрим вглубь
    div = soup.find('div', {'id': 'mw-subcategories'})
    if div:
        for li in div.findAll('li'):
            cat = {}
            cat['title'] = li.a.text.strip()
            cat['href'] = unquote(li.a['href'].strip())
            cat['type'] = 'category'
            cat['sub'] = parse_cats(cat['href'])
            result.append(cat)
    return result

def show_cat_struct(data, idx=0):
    for item in data:
        print('\t'*idx, item['title'], item['href'])
        if 'sub' in item:
            show_cat_struct(item['sub'], idx+1)


code = '/wiki/Категория:Готы'
# code = '/wiki/Категория:Культура_королевства_остготов'
data = parse_cats(code)
show_cat_struct(data)