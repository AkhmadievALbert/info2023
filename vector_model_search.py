import json
import operator
import os
import tools

from sklearn.metrics.pairwise import cosine_similarity
from tokenizer import Tokenizer
from tf_idf_calculator import TF_IDF_Calculator


def dist_cosine(vec_a, vec_b):
    cosine = cosine_similarity([vec_a], [vec_b])
    return cosine[0][0]


class VectorModelSearch:

    def get_results_array(input_array):
        output_dict = {"results": input_array}
        output_json = json.dumps(output_dict)
        return output_json

    def __init__(self):
        self.__tokenizer = Tokenizer()
        self.__all_docs_count = len(os.listdir(tools.LEMMATIZED_TEXTS_PATH))

        with open(tools.INDEX_PATH) as json_file:
            self.__indices = json.load(json_file)

        with open(tools.TF_IDF_PATH) as json_file:
            self.__tf_idf_calculations = json.load(json_file)

    def search(self, query):
        print("SEARCHING: {}".format(query))
        tokens = self.__tokenizer.clean_text(query)

        if len(tokens) == 0:
            print("Empty query")
            return

        print("LEMMATIZED: {}\n".format(' '.join(tokens)))
        query_vector = []
        corpus = list(self.__tf_idf_calculations.keys())

        for token in tokens:
            doc_with_terms_count = len(self.__tf_idf_calculations[token])
            _, _, tf_idf = TF_IDF_Calculator.calculate(token,
                                                       tokens,
                                                       self.__all_docs_count,
                                                       doc_with_terms_count)
            query_vector.append(tf_idf)

        distances = {}

        for index in self.__indices.keys():
            document_vector = []

            for token in tokens:
                try:
                    tf_idf = self.__tf_idf_calculations[token][index]["TF-IDF"]
                    document_vector.append(tf_idf)
                except KeyError:
                    document_vector.append(0.0)

            distances[index] = dist_cosine(query_vector, document_vector)

        searched_indices = sorted(distances.items(), key=operator.itemgetter(1), reverse=True)
        result = []
        for index in searched_indices:
            doc_id, tf_idf = index

            if tf_idf < 0.05:
                continue

            url = self.__indices[doc_id]
            result.append(url)
            print("Index: {}\nURL:{}\nCosine:{}\n".format(doc_id, url, tf_idf))

        output_dict = {"results": result}
        output_json = json.dumps(output_dict)
        print(result)
        print(output_json)
        return output_json