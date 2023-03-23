import nltk
import re

from nltk.corpus import stopwords
from pymystem3 import Mystem


class Tokenizer:

    def clean_text(self, text):
        tokens = self.__tokenize(text)
        tokens = self.__lemmatize(tokens)
        tokens = self.__remove_stop_words(tokens)

        return tokens

    @staticmethod
    def __tokenize(text):
        """ Делит текст на токены """
        tokens = nltk.word_tokenize(text)

        return tokens

    @staticmethod
    def __lemmatize(tokens):
        """ С помощью Mystem лемматизирует токены """
        mystem = Mystem()

        tokens = [token.replace(token, ''.join(mystem.lemmatize(token))) for token in tokens]

        return tokens

    @staticmethod
    def __remove_stop_words(tokens):
        """ Удаляет лишние символы """
        tokens = [re.sub(r"\W", "", token, flags=re.I) for token in tokens]

        stop_words = stopwords.words('russian')
        only_cyrillic_letters = re.compile('[а-яА-Я]')

        tokens = [token.lower() for token in tokens if (token not in stop_words)
                  and only_cyrillic_letters.match(token)
                  and not token.isdigit()
                  and token != '']

        return tokens