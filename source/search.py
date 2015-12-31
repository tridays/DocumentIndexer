# -*- coding: utf-8 -*-
__author__ = 'zhsl'
import os
from index import Index
from dictionary import Dictionary
from gama_encode import Gamma


class Search:

    def __init__(self, dic, inverted_index, document_num):
        self._dic = {}
        for i, x in enumerate(dic):
            self._dic[x] = i
        self._inverted_index = inverted_index
        self._document_num = document_num

    def search(self, search_info):
        """
        词项查找的主流程, 对查询内容分解
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
        """
        输出查询结果
        :param ret:
        :return:
        """
        if len(ret) == 0:
            print 'Sorry, No result!'
            return
        print '%d Docs retrieved:' % len(ret)
        for x in ret:
            print '\t%d: %s' % (x, self._document_num[x])

    def _search_reges(self, term):
        """
        查询词项是否存在词典中, 其中词典构建了 HASH 表,
        能快速的查询到词项
        :param term:
        :return:
        """
        if term in self._dic:
            return self._inverted_index[self._dic[term]]
        return []

    def _logic_process(self, result, logic):
        """
        对布尔查询的结果进行处理, 求每个查询词项的交集或者并集
        :param result:
        :param logic:
        :return:
        """
        flag = 0
        ret = set()
        for row in result:
            if logic is '&':
                if flag is 0:
                    flag = 1
                    ret = row
                else:
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
    inverted_index = Gamma.reade_inverted_index_encode(inverted_index_path)
    engine = Search(dic, inverted_index, document_num)
    # abate, abide, abject, able
    engine.search('  ab*te')
    engine.search('abate')
    engine.search('abate | a')

