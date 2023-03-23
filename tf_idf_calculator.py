import math

from tokenizer import Tokenizer


class TF_IDF_Calculator:

    @staticmethod
    def calculate(term, document_tokens_list, documents_count, documents_with_term_count):
        """
        Подсчитывает значение TF-IDF
        Большой вес в TF-IDF получат слова с высокой частотой в пределах
        конкретного документа и с низкой частотой употреблений в других документах.
        @param term: Слово
        @param document_tokens_list: Лемматизированный список слов документа
        @param documents_with_term_count: Число документов из коллекции, в которой встречается term
        @param documents_count: Число документов в коллекции
        @return: TF, IDF, TF * IDF
        """

        TF = document_tokens_list.count(term) / len(document_tokens_list)
        IDF = math.log(documents_count / documents_with_term_count)

        return round(TF, 6), round(IDF, 6), round(TF * IDF, 6)
