import math
import re
from math import log
from os import listdir
from os.path import isfile, join
import codecs
import nltk
import pymorphy2
from stop_words import get_stop_words
from bs4 import BeautifulSoup

def output_lemmas():
    stop_words = get_stop_words('ru')
    output_task1 = "../output/"
    output_task2 = "../output_task2/"

    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

    lemmatizer = pymorphy2.MorphAnalyzer(lang='ru')

    tokens_all = set()
    lemmas_all = {}

    for i in range(1, 101):
        print(i)
        tokens = list()
        html = codecs.open(output_task1 + 'page' + str(i) + '.txt', 'r', encoding='utf-8')
        try:
            data = html.read()
            text = BeautifulSoup(data, 'html.parser').get_text().lower()
            tokens += nltk.word_tokenize(text)
            tokens = [token for token in tokens if
                      token not in stop_words and re.match(r'^[а-яА-Я]+$', token) and not any(
                          char.isdigit() for char in token)]

        except:
            continue

        lemmas = {}

        cleaning1 = set()
        for word in tokens:
            try:
                if word.isalpha() and not re.match(r"[a-z]", word):
                    cleaning1.add(word)
            except:
                continue

        cleaning2 = set()
        for word in cleaning1:
            try:
                if not word in get_stop_words("ru"):
                    cleaning2.add(word)
            except:
                continue

        for token in cleaning2:
            lemma = lemmatizer.parse(token)[0].normal_form
            if lemmas.keys().__contains__(lemma):
                lemmas[lemma] += [token]
            else:
                lemmas[lemma] = [token]

        lemmas_all.update(lemmas)
        tokens_all.update(cleaning2)
        lemmas_file = open(output_task2 + 'lemmas' + str(i) + '.txt', 'w')
        for lemma in lemmas:
            tokens = ' '
            for token in lemmas[lemma]:
                tokens += ' ' + token
            lemmas_file.write(lemma + ":" + tokens + '\n')
        lemmas_file.close()

    tokens_file = open(output_task2 + 'tokens.txt', 'w')
    for token in tokens_all:
        tokens_file.write(token + "\n")
    tokens_file.close()

    lemmas_all_file = open(output_task2 + 'lemmas.txt', 'w')
    for lemma in lemmas_all:
        tokens = ' '
        for token in lemmas_all[lemma]:
            tokens += ' ' + token
        lemmas_all_file.write(lemma + ":" + tokens + '\n')
    lemmas_all_file.close()


def find_tf_and_idf():
    stop_words = get_stop_words('ru')
    output_task1 = "../output/"
    output_task2 = "../output_task2/"
    output_task4 = "../output_task4/"

    lemmatizer = pymorphy2.MorphAnalyzer(lang='ru')

    for i in range(1, 101):
        try:
            text_file = open(output_task1 + 'page' + str(i) + '.txt', 'r', encoding='utf-8')
            text = BeautifulSoup(text_file, 'html.parser').get_text().lower()
            text = re.sub(r'\W+', ' ', text)
            tokens = nltk.word_tokenize(text)
            tokens = [token for token in tokens if
                      token not in stop_words and re.match(r'^[а-яА-Я]+$', token) and not any(
                          char.isdigit() for char in token)]

        except:
            continue

        # tf for tokens
        tokens_set = set(tokens)
        tokens_tf_dict = dict.fromkeys(tokens_set, 0.0)
        tokens_count = len(tokens)
        for token in tokens:
            tokens_tf_dict[token] += 1
        for k, v in tokens_tf_dict.items():
            tokens_tf_dict[k] = float(v) / float(tokens_count)

        # idf for tokens
        tokens_idf_dict = dict.fromkeys(tokens_set, 0.0)
        N = 100

        for j in range(100):

            try:
                tokens_in_file = [token.split(':') for token in
                                  open(output_task2 + 'tokens' + str(j) + '.txt').read().splitlines()]
                tokens_in_file = [element[0] for element in tokens_in_file]
                for word in tokens_in_file:
                    if word in tokens_set:
                        tokens_idf_dict[word] += 1.0
            except:
                continue

        for k, v in tokens_tf_dict.items():
            tokens_idf_dict[k] = math.log(N / float(v))

        print(tokens_tf_dict)
        print(tokens_idf_dict)

        lemmas = list()
        for token in tokens:
            lemmas.append(lemmatizer.parse(token)[0].normal_form)

        lemmas_set = set(lemmas)
        lemmas_tf_dict = dict.fromkeys(lemmas_set, 0.0)
        lemmas_count = len(lemmas)
        for lemma in lemmas:
            lemmas_tf_dict[lemma] += 1
        for k, v in lemmas_tf_dict.items():
            lemmas_tf_dict[k] = float(v) / float(lemmas_count)

        lemmas_idf_dict = dict.fromkeys(lemmas_set, 0.0)
        N = 100

        for j in range(100):
            try:
                lemmas_in_file = [lemma.split(':') for lemma in
                                  open(output_task2 + 'lemmas' + str(j) + '.txt').read().splitlines()]
                lemmas_in_file = [element[0] for element in lemmas_in_file]
                for word in lemmas_in_file:
                    if word in lemmas_set:
                        lemmas_idf_dict[word] += 1.0
            except:
                continue

        for k, v in lemmas_tf_dict.items():
            lemmas_idf_dict[k] = math.log(N / float(v))

        print(lemmas_tf_dict)
        print(lemmas_idf_dict)

        tokens_file = open(output_task4 + 'tokens_tf_idf' + str(i) + '.txt', 'w')
        for k, v in tokens_tf_dict.items():
            tokens_file.write(str(k) + ": " + str(tokens_tf_dict[k]) + " " + str(tokens_idf_dict[k]) + "\n")

        lemmas_file = open(output_task4 + 'lemmas_tf_idf' + str(i) + '.txt', 'w')
        for k, v in lemmas_tf_dict.items():
            lemmas_file.write(str(k) + ": " + str(lemmas_tf_dict[k]) + " " + str(lemmas_idf_dict[k]) + "\n")


if __name__ == '__main__':
    # output_lemmas()
    find_tf_and_idf()
