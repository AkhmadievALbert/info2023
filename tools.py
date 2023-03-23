import os
import shutil


BASE_URL = "https://ru.wikipedia.org"
NESTED_LINK_REGEXP = "^/wiki/"
INDEX_PATH = "output/index.json"
TEXT_DOCUMENTS_PATH = "output/text_documents"
LEMMATIZED_TEXTS_PATH = "output/lemmatized_texts"
INVERTED_INDEX_PATH = "output/inverted_index.json"
TF_IDF_PATH = "output/td-idf-calculation.json"

def prepare_output_directory(path):
    """ Очищает папку output от файлов предыдущего запуска """
    try:
        shutil.rmtree(path)
    except OSError:
        print("Directory %s is deleted" % path)

    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory '%s' " % path)


def save_text_in_file(text_file_path, text):
    text_file = open(text_file_path, "w")
    text_file.write(text)
    text_file.close()