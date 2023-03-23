import json

from bs4 import BeautifulSoup
from bs4.element import Comment

import os
import tools
import shutil
import urllib.request
import re


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def get_html(url):
    """
    Возвращает HTML документ по переданному URL
    :param url: URL сайта
    :return: HTML документ
    """
    try:
        response = urllib.request.urlopen(url)
        return response.read()
    except:
        return None


class Spider:

    def __init__(self,
                 base_url,
                 nested_link_regexp,
                 max_pages_count=100,
                 min_words_count=1200,
                 output_directory="output/",
                 output_filename="index.json"):
        """
        Конструктор
        :param base_url: Базовый URL, с которого начинается работа краулера
        :param nested_link_regexp: Регулярка
        :param max_pages_count: Максимальное количество обработанных страниц
        :param min_words_count: Минимальное кол-во слов на странице
        :param output_directory: Директория для сохранения документов
        :param output_filename: Имя файла, в который записывается индекс страницы и ее URL
        """
        self.__base_url = base_url
        self.__nested_link_regexp = nested_link_regexp
        self.__max_pages_count = max_pages_count
        self.__min_words_count = min_words_count
        self.__output_directory = output_directory
        self.__output_filename = output_filename
        self.__current_page_index = 0
        self.__queue = []
        self.__parsed_urls = set()
        self.__index = {}
        self.html_documents_path = "%s/text_documents/" % self.__output_directory

    def start_parsing(self):
        """ Производит парсинг с начальной страницы """
        tools.prepare_output_directory(self.__output_directory)

        os.mkdir(self.html_documents_path)

        self.__queue.append(self.__base_url)

        while self.__queue and self.__current_page_index < self.__max_pages_count:
            url = self.__queue.pop()
            html = get_html(url)

            if html is None:
                continue

            soup = BeautifulSoup(html, 'html.parser')
            words_list = self.__get_visible_words_list(soup)

            self.__parsed_urls.add(url)
            print('Processing %s ...' % url)

            if len(words_list) >= self.__min_words_count:
                text = u" ".join(t.strip() for t in words_list)
                self.__save_text(self.__current_page_index, url, text)
                self.__current_page_index += 1
                print('Saved {} - {}'.format(self.__current_page_index, url))

            nested_links = list(filter(self.__is_handled, self.__get_nested_links(soup)))
            self.__queue.extend(nested_links)

        self.__save_index()
        print("Done!")

    def __is_handled(self, url):
        return not (url in self.__parsed_urls)

    def __get_nested_links(self, soup):
        """
        Возвращает массив вложенных ссылок
        """
        internal_references = soup.findAll('a', attrs={'href': re.compile(self.__nested_link_regexp)})
        links = list(set([self.__base_url + item['href'] for item in internal_references]))
        return links

    @staticmethod
    def __get_visible_words_list(soup):
        """
        Проверяет количество слов на странице
        :return: True, если слов не меньше self.__min_words_count
        """
        texts = soup.findAll(text=True)
        visible_texts = list(filter(tag_visible, texts))
        return visible_texts

    def __save_text(self, index, url, text):
        """
        Сохраняет переданный текстовый документ и
        добавляет в таблицу URL с индексом
        :param index: Индекс страницы
        :param index: URL страницы
        :param text: HTML документ
        """

        html_filename_path = "%s/%d.txt" % (self.html_documents_path, index)
        tools.save_text_in_file(html_filename_path, text)
        self.__index[index] = url

    def __save_index(self):
        dump = json.dumps(self.__index,
                          sort_keys=False,
                          indent=4,
                          ensure_ascii=False,
                          separators=(',', ': '))

        tools.save_text_in_file(self.__output_directory + self.__output_filename, dump)