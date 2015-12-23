# -*- coding: utf-8 -*-
__author__ = 'zhsl'
import os
from index import Index
from dictionary import Dictionary
from gama_encode import Gama


class Search:

    def __init__(self, dic, inverted_index, document_num):
        self._dic = {}
        for i, x in enumerate(dic):
            self._dic[x] = i
        self._inverted_index = inverted_index
        self._document_num = document_num

    def search(self, search_info):
        """
        :param search_info:
        :return:
        """
        print 'Begin searching ...'
        search_info = search_info.strip(' ')
        terms = search_info.split(' ')
        logic = ''
        for term in terms:
            if term == '&' or term == '|':
                logic = term
                terms.remove(term)
        ret_temp = []
        for term in terms:
            ret_temp.append(set(self._search_reges(term)))
        ret = []
        if len(ret_temp) != 0:
            if logic != '':
                ret_temp = self._logic_process(ret_temp, logic)
            ret = sorted(ret_temp[0])
        self._print_result(ret)

    def _print_result(self, ret):
        if len(ret) == 0:
            print 'Sorry, No result!'
            return
        print '%d Docs retrieved:' % len(ret)
        for x in ret:
            print '\t%d: %s' % (x, self._document_num[x])

    def _search_reges(self, term):
        if term in self._dic:
            return self._inverted_index[self._dic[term]]
        return []

    def _logic_process(self, result, logic):
        ret = set()
        for row in result:
            if logic is '&':
                ret &= row
            elif logic is '|':
                ret |= row
        return [ret]


if __name__ == '__main__':
    file_dir = os.path.join(os.getcwd(), '../data/document')
    dic_path = os.path.join(os.getcwd(), '../data/index/dictionary')
    inverted_index_path = os.path.join(os.getcwd(), '../data/index/doc_index_encode')
    ind = Index(file_dir)
    ind.build_index()
    dic = Dictionary.read_dictionary(dic_path)
    document_num = ind.get_document_num()
    print document_num
    inverted_index = Gama.reade_inverted_index_encode(inverted_index_path)
    engine = Search(dic, inverted_index, document_num)
    # abate, abide, abject, able
    engin.search('  ab*te')
    engin.search('abate')
    engin.search('abate | a')

