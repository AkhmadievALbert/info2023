from spider import Spider

# if __name__ == '__main__':
#     base_url = "https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/bs4ru.html"
#     nested_link_class = "reference internal"
#     spider = Spider(base_url, nested_link_class)
#     spider.start_parsing()

import requests
from bs4 import BeautifulSoup
import re
import os
import pymorphy2
import nltk
from stop_words import get_stop_words
nltk.download('punkt')

# Инициализируем анализатор морфологии
morph = pymorphy2.MorphAnalyzer()

# Список стоп-слов (союзов, предлогов, чисел)
# stop_words = ['без', 'бы', 'был', 'была', 'были', 'было', 'быть', 'в', 'вам', 'вас', 'весь', 'во', 'вот', 'все', 'всего', 'всей', 'вы', 'да', 'для', 'до', 'его', 'ее', 'ей', 'ему', 'если', 'есть', 'еще', 'же', 'за', 'и', 'из', 'или', 'им', 'их', 'к', 'как', 'ко', 'когда', 'кто', 'ли', 'либо', 'между', 'меня', 'мне', 'много', 'может', 'мы', 'на', 'над', 'нам', 'нами', 'нас', 'наш', 'не', 'него', 'нее', 'ней', 'нет', 'ни', 'них', 'но', 'ну', 'о', 'об', 'однако', 'он', 'она', 'они', 'оно', 'от', 'очень', 'по', 'под', 'при', 'с', 'со', 'так', 'также', 'такой', 'те', 'тебя', 'тем', 'то', 'того', 'тоже', 'той', 'только', 'том', 'ты', 'у', 'уже', 'хотя', 'чего', 'чей', 'чем', 'что', 'чтобы', 'чье', 'чья', 'эта', 'эти', 'это', 'я']
stop_words = get_stop_words('ru')
urls = []
def fill_urls():
    for i in range(1, 11):
        urls.append(f"https://habr.com/ru/post/{i}")

def get_contents():
    # Создаем директорию для файлов, если она не существует
    if not os.path.exists('output'):
        os.makedirs('output')

    # Список страниц для загрузки

    # Создаем файл index.txt
    with open('index.txt', 'w', encoding='utf-8') as f:
        for i, url in enumerate(urls):
            # Получаем содержимое страницы
            response = requests.get(url)
            content = response.content

            # Парсим содержимое страницы и сохраняем его в файл
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text().lower()
            text = re.sub(r'\s+', ' ', text)  # удаляем лишние пробелы и переносы строк
            filename = f'output/page{i + 1}.txt'
            with open(filename, 'w', encoding='utf-8') as page_file:
                page_file.write(text)

            # Записываем номер файла и ссылку на страницу в файл index.txt
            f.write(f'{i + 1}. {url}\n')

# Функция для получения списка токенов из файла
def get_tokens(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
        # Удаляем лишние символы
        text = re.sub(r'\W+', ' ', text)
        # Токенизируем текст
        tokens = nltk.word_tokenize(text)
        # Отфильтровываем стоп-слова и "мусор"
        tokens = [token for token in tokens if token not in stop_words and re.match(r'^[а-яА-Я]+$', token) and not any(char.isdigit() for char in token)]
        # Лемматизируем токены
        # lemmas = [morph.parse(token)[0].normal_form for token in tokens]
        # Оставляем только уникальные леммы
        unique_lemmas = set(tokens)
        return list(unique_lemmas)

inverted_index = {}
def get_lemmas():
    tokens = []
    for i, url in enumerate(urls):
        filename = os.path.join("output", 'page{}.txt'.format(i + 1))
        # Получаем список токенов из файла
        file_tokens = get_tokens(filename)
        # Добавляем токены в общий список
        tokens += file_tokens
        for token in file_tokens:
            lemma = morph.parse(token)[0].normal_form
            if lemma in inverted_index:
                inverted_index[lemma].add(i + 1)
            else:
                inverted_index[lemma] = {i + 1}

    tokens = set(tokens)
    # Группируем токены по леммам
    lemmas = {}
    for token in tokens:
        lemma = morph.parse(token)[0].normal_form
        if lemma in lemmas:
            lemmas[lemma].append(token)
        else:
            lemmas[lemma] = [token]

    with open('inverted_index.txt', 'w', encoding='utf-8') as f:
        for key in sorted(inverted_index.keys()):
            f.write(key + ': ' + ', '.join(f'{inverted_index[key]}') + '\n')

    with open('tokens.txt', 'w', encoding='utf-8') as f:
        for token in sorted(tokens):
            f.write(token + ' ')

    with open('grouped_tokens.txt', 'w', encoding='utf-8') as f:
        for lemma in sorted(lemmas.keys()):
            f.write(lemma + ': ' + ', '.join(lemmas[lemma]) + '\n')

def create_inverted_index():
    for i, url in enumerate(urls):
        filename = os.path.join("output", 'page{}.txt'.format(i + 1))
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
            tokens = re.findall(r'\b\w+\b', text.lower())
            for token in set(tokens):
                if token.isdigit():
                    continue
                if token in stop_words:
                    continue
                if not token.isalpha():
                    continue
                if any(c.isdigit() for c in token):
                    continue
                lemma = morph.parse(token)[0].normal_form
                print(inverted_index)
                if lemma in inverted_index:
                    inverted_index[lemma].add(i + 1)
                else:
                    inverted_index[lemma] = {i + 1}
    with open('inverted_index.txt', 'w', encoding='utf-8') as f:
        for key in sorted(inverted_index.keys()):
            f.write(key + ': ' + ', '.join(inverted_index[key]) + '\n')

# Реализуем булев поиск
def boolean_search(query):
    query = query.lower().split()
    results = set(range(1, len(urls) + 1))
    for term in query:
        if term == 'and':
            continue
        elif term == 'or':
            continue
        elif term == 'not':
            continue
        else:
            if term in inverted_index:
                results &= inverted_index[term]
            else:
                results &= set()
    for i, term in enumerate(query):
        if term == 'and':
            if query[i-1] in inverted_index and query[i+1] in inverted_index:
                results &= inverted_index[query[i-1]] & inverted_index[query[i+1]]
        elif term == 'or':
            if query[i-1] in inverted_index and query[i+1] in inverted_index:
                results |= inverted_index[query[i-1]] | inverted_index[query[i+1]]
        elif term == 'not':
            if query[i+1] in inverted_index:
                results -= inverted_index[query[i+1]]
    return sorted(results)

if __name__ == '__main__':
    fill_urls()
    # get_contents()
    get_lemmas()
    # create_inverted_index()
    print(inverted_index)
    print(boolean_search("следующий and сайт"))