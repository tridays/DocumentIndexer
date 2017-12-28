__author__ = 'xp'

import os

from src.parser import Parser
from src.tokenizer import Tokenizer


class TermProvider(object):
    def __init__(self, trec_dir, stopword_file):
        parser = Parser()
        for filename in os.listdir(trec_dir):
            try:
                with open(os.path.join(trec_dir, filename), 'r') as f:
                    parser.load(f.read())
            except Exception as e:
                pass
        self.docs = parser.docs

        with open(stopword_file, 'r') as f:
            stopwords = f.readlines()
        self.tokenizer = Tokenizer(stopwords)

    def __iter__(self):
        return self.tokenizer.iter_terms(self.docs)


if __name__ == '__main__':
    provider1 = TermProvider('../assets/trecs', '../assets/index/stop_words')
    iter1 = iter(provider1)
    for i in range(5):
        print(i, next(iter1))
