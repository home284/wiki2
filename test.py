import requests
from bs4 import BeautifulSoup
import json
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import SnowballStemmer
from nltk.metrics import distance
from nltk.corpus import stopwords
import pymorphy2
import string
import re

HOST = 'https://ru.wikipedia.org/wiki'

session = requests.Session()

def get_page_categories(page):
    soup = BeautifulSoup(session.get(HOST+'/'+page).text, 'html.parser')
    cats = soup.find('div', {'class': 'catlinks'}).ul
    for li in cats.findAll('li'):
        print(li.a['title'], li.a.text, li.a['href'])

def parse_page(page):
    pass

def get_page_summary(page):
    data = json.loads(session.get('https://ru.wikipedia.org/api/rest_v1/page/summary/'+page).text)
    return data

sw = stopwords.words('russian')
morph = pymorphy2.MorphAnalyzer()
ss = SnowballStemmer(language='russian')

def get_title(value):
    eng = 'abcdefghijklmnopqrstuvwxyz'
    if sum([value['title'].lower().count(l) for l in eng])/len(value) >= .3:
        return re.search(r'^(.+?)\s*—', value['extract']).group(1)
    else: return value['title']

def hide_word(text, words):
    """ Заменяет слова words знаками вопроса для теста """
    start_word = words
    eng = 'abcdefghijklmnopqrstuvwxyz'
    words_to_replace = []
    text = text.replace('́', '')
    words = re.sub(r'\(.*?\)', '', words).strip()
    words = [words] + re.split(r'[\s\.\,«»]+', words)
    norm_words = [morph.parse(word) for word in words]
    for word in word_tokenize(text):
        for a in norm_words:
            for a1 in a:
                for b in morph.parse(word):
                    # print(
                    #     word, a1.normal_form, b.normal_form,
                    #     distance.edit_distance(a1.normal_form, b.normal_form),
                    #     distance.jaro_similarity(a1.normal_form, b.normal_form),
                    #     distance.jaro_winkler_similarity(a1.normal_form, b.normal_form),
                    # )
                    #print(word, a1.normal_form, b.normal_form, ss.stem(word), a1.normal_form == b.normal_form)
                    if a1.normal_form == b.normal_form:
                        words_to_replace.append(word)
                    elif ss.stem(a1.normal_form) == ss.stem(b.normal_form):
                        words_to_replace.append(word)
                    elif distance.jaro_winkler_similarity(a1.normal_form, b.normal_form) >= 0.80:
                        words_to_replace.append(word)
    words_to_replace = list(set(words_to_replace + [start_word]))
    # print(words_to_replace)
    # print(sorted(words_to_replace, key=len, reverse=True))
    for w in sorted(words_to_replace, key=len, reverse=True):
        text = text.replace(w, '???')
    text = re.sub(r'[\?\»][\?\s]+[\?\»]', '???', text)
    return text

# def get_rand_sent(text)

page = 'Азаров,_Сергей_Семёнович'

# str = "Готы - древнегерманский союз племён. С II века н. э. до VIII века н. э. играл значительную роль в истории Европы. Это было объединение германских племён, вероятно, скандинавского происхождения, говоривших на восточногерманском готском языке (для которого епископ Ульфила в IV веке н. э. разработал готское письмо). В первые века нашей эры они начали путь от Скандинавского полуострова и постепенно расселились к Северному Причерноморью и реке Дунай, достигнув аванпостов Римской империи. В IV веке среди готов распространилось христианство."
# Замена слова в тексте
# text = hide_word(str, 'Готы')
# print(text)

# res = get_page_categories(page)
# parse_page(page)

res = get_page_summary(page)
title = get_title(res)
text = res['extract']
print(res)

print(title)
text = hide_word(text, title)
print(text)

