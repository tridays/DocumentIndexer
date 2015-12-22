# -*- coding: utf-8 -*-
__author__ = 'zhsl'
import os


class Token:

    def __init__(self):
        stop_words_path = os.getcwd() + '/../data/stop_words'
        self._stop_words = set()
        with open(stop_words_path, 'r') as data:
            for word in data:
                self._stop_words.add(word[:-1])

    def get_term(self, token):
        """
        得到词条对应的词项( term )
        :param token:
        :return:
        """
        term = []
        for i, word in enumerate(token):
            # if word in self._stop_words:
            #     continue
            term.append((word, i))
        return term


    def is_stop_words(self, token):
        """
        判断 word 是否为 听用词
        :param word:
        :return:
        """
        if self.get_term(token) in self._stop_words:
            return True
        return False

if __name__ == '__main__':
    tk = Token()