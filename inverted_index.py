import nltk
import json
import os
import math
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from collections.abc import  Mapping

nltk.download('punkt')
nltk.download('stopwords')


def cosine(q, doc):
    return np.sum(np.cos(q, doc))


def get_nro_words_by_id(id_text):
    open_file = open('index_nro_words.txt', 'r')
    line = open_file.readline()
    while line:
        json_data = json.loads(line[:-1])
        if str(json_data[0]) == str(id_text):
            return json_data[1]
        else:
            line = open_file.readline()
    return None


def filter_stop(text):
    if isinstance(text, Mapping):
        to_make = text['text']
    else:
        to_make = text
    tokens = nltk.word_tokenize(to_make)
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


def filter_stop_text(text):
    if isinstance(text, Mapping):
        to_make = text['text']
    else:
        to_make = text
    tokens = nltk.word_tokenize(to_make)
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
    return [tokens_clean]


def token_reduction(tokens_clean):
    list_words = []
    open_ext = open('index_nro_words.txt', 'a')
    stemmer = SnowballStemmer('spanish')
    for list_to in tokens_clean:
        nro_word_id = len(list_to[0])
        dict_nro = (list_to[1], nro_word_id)
        open_ext.write(json.dumps(dict_nro) + '\n')
        for word in list_to[0]:
            steam_word = stemmer.stem(word)
            list_words.append([steam_word, list_to[1]])
    list_words.sort()
    return list_words


def token_reduction_text(tokens_clean):
    list_words = []
    stemmer = SnowballStemmer('spanish')
    for list_to in tokens_clean:
        for word in list_to:
            steam_word = stemmer.stem(word)
            list_words.append(steam_word)
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


def construct_index_norm(file_tf_idf_index, file_norm_index):
    index_read = open(file_tf_idf_index, 'r')
    norm_index = open(file_norm_index, 'a')
    line_index_read = index_read.readline()
    while line_index_read:
        json_line = json.loads(line_index_read[:-1])
        for key, value in json_line[1].items():
            int_magnitude = get_nro_words_by_id(key)
            json_line[1][str(key)] = math.log10(value + 1) * math.log10(int_magnitude/value)
        line_index_read = index_read.readline()
        norm_index.write(json.dumps(json_line) + '\n')
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


def get_terms(query_text):
    words_query = {}
    tokens = filter_stop_text(query_text)
    token_clean = token_reduction_text(tokens)
    magnitude = len(token_clean)
    for word in token_clean:
        if word in words_query:
            words_query[word] = words_query[word] + 1
        else:
            words_query[word] = 1
    for key, value in words_query.items():
        words_query[str(key)] = math.log10(value + 1) * math.log10(magnitude / value)
    return words_query, token_clean


def get_just_index(query_words):
    ans = []
    for value in query_words:
        for key in value[1].keys():
            if key not in ans:
                ans.append(key)
    return ans


def made_word(data_index, index):
    ans = []
    for key in index:
        partial = []
        for word in data_index:
            if key in word[1].keys():
                partial.append(word[1][key])
            else:
                partial.append(0)
        ans.append(partial)
    return ans


def make_score(query_terms):
    values = []
    for key, value in query_terms.items():
        values.append(value)
    result = np.array(values)
    return result


class InvertedIndex:
    index_file_name = ""
    index_norm_name = ""
    texts = []
    stemmer = SnowballStemmer('spanish')

    def __init__(self, file, texts_list):
        self.index_file_name = file
        self.index_norm_name = file + '.norm'
        for text in texts_list:
            self.texts.append(text)

    def get_index_words(self, list_words):
        open_dict = open('norm_index.txt', 'r')
        ans_dict = []
        line = open_dict.readline()
        iter = 0
        while line:
            json_data = json.loads(line[:-1])
            if json_data[0] == list_words[iter]:
                iter = iter + 1
                ans_dict.append(json_data)
                if iter == len(list_words):
                    break
            line = open_dict.readline()
        return ans_dict

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

    def generate_index_no_memory(self):
        list_word_n = []
        token_clean = []
        file = open(self.index_file_name, "a")
        for book in self.texts:
            with open(book, encoding='utf-8') as f:
                words = json.load(f)
            for element in words:
                token_clean.append(filter_stop(element))
            list_words = token_reduction(token_clean)
            list_word_n.append(list_words)
        final = construct_index_tf_idf_no_memory_management(list_word_n)
        for data in final:
            file.write(json.dumps(data) + '\n')
        construct_index_norm(self.index_file_name, self.index_norm_name)

    def retrieval(self, query_text, k):
        result = []
        (query_words, tokens) = get_terms(query_text)
        data_index = self.get_index_words(tokens)
        keys_data = get_just_index(data_index)
        words_to = made_word(data_index, keys_data)
        query = make_score(query_words)
        for i in range(len(words_to)):
            sim = cosine(np.array(query) * 10, np.array(words_to[i]) * 10)
            result.append((keys_data[i], sim))  # [ (doc1, sc1), (doc, sc2) ]
        result.sort(key=lambda x:x[1])
        return result[0:k]
