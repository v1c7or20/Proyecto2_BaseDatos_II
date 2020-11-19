from inverted_index import *

if __name__ == '__main__':
    ind = InvertedIndex('index.txt', ['data_mid.json'])
    ind.retrieval('basic is best', 3)
# completed
