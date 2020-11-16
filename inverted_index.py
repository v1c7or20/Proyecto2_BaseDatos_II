import nltk
import json
import os
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

nltk.download('punkt')
nltk.download('stopwords')


def filter_stop(text):
    tokens = nltk.word_tokenize(text['text'])
    stop_list = stopwords.words("spanish")
    list_words = open("stoplist.txt").read()
    list_words = list_words.split("\n")
    for word in list_words:
        if not (word in stop_list):
            stop_list.append(word)
    stop_list += ['?', "'", '$', '%', '&', '#', '«', '”', '…', '-', '..', '...', 'aqui', '.', ',', ";", ":", "(", ")", "''", "´´", "!", "¡", "@", "RT", "Lo", "En", "Ha"]
    tokens_clean = tokens.copy()
    for token in tokens:
        if token in stop_list:
            tokens_clean.remove(token)
    return [tokens_clean, text['id']]


def token_reduction(tokens_clean):
    list_words = []
    stemmer = SnowballStemmer('spanish')
    for list_to in tokens_clean:
        for word in list_to[0]:
            steam_word = stemmer.stem(word)
            list_words.append([steam_word, list_to[1]])
    list_words.sort()
    return list_words


def construct_index_tf_idf_no_memory_management(book_list):
    final_index = []
    i = 0
    for word_list in book_list:
        i = i + 1
        for word in word_list:
            make = True
            for elem in final_index:
                if elem[0] == word[0]:
                    if str(word[1]) in elem[1]:
                        elem[1][str(word[1])] = elem[1][str(word[1])] + 1
                    else:
                        elem[1][str(word[1])] = 1
                    make = False
            if make:
                index = [word[0], {str(word[1]): 1}]
                final_index.append(index)
    return final_index


def construct_index_tf_idf(book_list, file_index):
    i = 0
    file = open(file_index, "a")
    for word_list in book_list:
        i = i + 1
        for word in word_list:
            index = [word[0], {str(word[1]): 1}]
            file.write(json.dumps(index) + '\n')


def construct_index_norm(book_list):
    pass


def join_block(json_data):
    ans_dict = []
    i = 0
    for data in json_data:
        i = i + 1
        for to_compare in json_data[i:]:
            if data[0] == to_compare[0]:
                for key, value in to_compare[1].items():
                    if str(key) in data[1]:
                        data[1][str(key)] = data[1][str(key)] + to_compare[1][str(key)]
                    else:
                        data[1][str(key)] = to_compare[1][str(key)]
                to_compare[1].clear()
    for data in json_data:
        if len(data[1]) > 0:
            ans_dict.append(data)
        ans_dict.sort(key=lambda x: x[0])
    return ans_dict


def blocked_sort_based_index(file_index, nro_buffers):
    file_read = open(file_index, "r")
    temp_write = open(file_index + '.tmp', 'a')
    line = {}
    for i in range(nro_buffers):
        line[i] = file_read.readline()
    while line[0]:
        json_data = []
        for i in range(nro_buffers):
            if len(line[i][:-1]) > 0:
                json_data.append(json.loads(line[i][:-1]))
        data_join = join_block(json_data)
        for join in data_join:
            if len(join) > 0:
                temp_write.write(json.dumps(join) + '\n')
        for i in range(nro_buffers):
            line[i] = file_read.readline()
    file_read.close()
    temp_write.close()
    os.remove(file_index)
    os.rename('./' + file_index + '.tmp', file_index)
    pass


class InvertedIndex:
    index_file_name = ""
    texts = []
    stemmer = SnowballStemmer('spanish')

    def __init__(self, file, texts_list):
        self.index_file_name = file
        for text in texts_list:
            self.texts.append(text)

    def write_index(self, file_index):
        file = open(self.index_file_name, "w")
        file.write(json.dumps(file_index))

    def generate_index(self):
        list_word_n = []
        token_clean = []
        for book in self.texts:
            with open(book, encoding='utf-8') as f:
                words = json.load(f)
            for element in words:
                token_clean.append(filter_stop(element))
            list_words = token_reduction(token_clean)
            list_word_n.append(list_words)
        construct_index_tf_idf(list_word_n, "file_try.json")
