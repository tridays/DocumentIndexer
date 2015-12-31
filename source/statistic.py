# -*- coding: utf-8 -*-
__author__ = 'zhsl'


class Statistic:

    def __init__(self):
        self._term_cnt = 0
        self._doc_cnt = 0
        self._doc_term = {}
        return

    def input_term_doc(self, term, doc):
        self._term_cnt += 1
        if doc not in self._doc_term:
            self._doc_cnt += 1
            self._doc_term[doc] = 0
        self._doc_term[doc] += 1
        return

    def display_statistic(self):
        print 'the number of the document: %d' % (self._doc_cnt)
        print 'the number of the term: %d' % (self._term_cnt)
        print 'the average length of document: %d' % (self._term_cnt / self._doc_cnt)
        return
