import os
import json
import tools


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class InvertedIndexFactory:

    def __init__(self, input_directory_path, output_filename):
        self.__input_directory_path = input_directory_path
        self.__output_filename = output_filename
        self.__inverted_index = {}

    def make_inverted_index(self):
        """ Создает инвертированный список на основе файлов из заданной директории"""
        all_files = os.listdir(self.__input_directory_path)

        for (index, filename) in enumerate(all_files):
            print("{}/{}".format(index, len(all_files)))
            input_file_path = self.__input_directory_path + '/' + filename
            with open(input_file_path, 'r') as file:
                index = filename.split('.')[0]
                text = file.read().split(' ')
                for word in text:
                    try:
                        self.__inverted_index[word].add(index)
                    except KeyError:
                        self.__inverted_index[word] = {index}

        self.__save_inverted_index_to_json()

    def __save_inverted_index_to_json(self):
        dump = json.dumps(self.__inverted_index,
                          sort_keys=False,
                          indent=4,
                          ensure_ascii=False,
                          separators=(',', ': '),
                          cls=SetEncoder)

        tools.save_text_in_file(self.__output_filename, dump)
