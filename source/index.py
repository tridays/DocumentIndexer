# -*- coding: utf-8 -*-
__author__ = 'zhsl'
import os
import heapq
import csv
from stream import TokenStream
from gama_encode import Gamma
from dictionary import Dictionary
from statistic import Statistic


class Index:

    def __init__(self, document_path, max_block=10000):
        self._dir_path = os.path.dirname(document_path)
        self._index_block_dir = os.path.join(self._dir_path, 'index_block')
        self._index_block_path = []
        self._token_stream = TokenStream(document_path)
        self._stream_is_empty = False
        self._max_block = max_block
        self._statistic = Statistic()
        return

    def get_document_num(self):
        """
        获取文档对应的编号
        :return:
        """
        return self._token_stream.get_document_num()

    def _spimi_invert(self):
        """
        SPIMI 算法构建索引块
        single-pass in-memory indexing
        :return:
        """
        term_dic = {}
        term_cnt = 0
        inverted_index = []
        block_size = 0
        while block_size < self._max_block:
            ret = self._token_stream.next_term_docid()
            if ret is None:
                self._stream_is_empty = True
                break
            self._statistic.input_term_doc(ret[0], ret[-1])
            term, term_position, doc_id = ret
            if term not in term_dic:
                term_dic[term] = term_cnt
                inverted_index.append([doc_id])
                term_cnt += 1
            else:
                position = term_dic[term]
                if doc_id != inverted_index[position][-1]:
                    inverted_index[position].append(doc_id)
            block_size += 1
        return term_dic, term_cnt, inverted_index

    def build_index(self):
        """
        构建文档的倒排记录表和词典, 通过 SPIMI 算法来构建
        主要分为两个步骤: 1. 构建索引块  2. 合并索引块
        在合并的时候, 写入磁盘的过程中, 对词典进行单一字符串的压缩,
        对倒排记录表进行 Gamma 编码压缩
        :return:
        """
        # 构建索引块
        print '\tPhase 1: create index block, each block has at most 10000 term-docids'
        self._build_index_block()
        # 合并每个索引块, 构建全局索引
        print '\tPhase 2: merge each index block'
        dic, inverted_index = self._build_global_index()
        Dictionary.write_dictionary(dic, os.path.join(
                                    self._dir_path, 'index/dictionary'))
        Gamma.write_inverted_index_encode(inverted_index, os.path.join(
                                self._dir_path, 'index/doc_index_encode'))
        return

    def _build_global_index(self):
        """
        合并 SPIMI 算法第一步生成的索引块, 每次从磁盘中读取每个倒排记录表的一部分,
        然后把相同词项的倒排记录合并, 然后维护一个优先队列, 为字典序优先级,
        每次读取优先级最高的词项写入到磁盘中
        :return:
        """
        block_dic = []
        block_doc_csv = []
        for block_path in self._index_block_path:
            with open(block_path + '_dic', 'r') as block_dic_file:
                block_dic.append(Dictionary.decompression(block_dic_file.read()))
            block_doc_csv.append(csv.reader(open(block_path + '_doc', 'r'), delimiter=' '))
        dic_point = [0] * len(block_dic)
        dic_heap = []
        term_dic = []
        term_doc = []
        heapq.heapify(dic_heap)
        while True:
            flag = True
            for i in range(len(block_dic)):
                if dic_point[i] >= len(block_dic[i]):
                    continue
                flag = False
                term = block_dic[i][dic_point[i]]
                if term in dic_heap:
                    continue
                else:
                    heapq.heappush(dic_heap, term)
            if flag:
                break
            top_term = heapq.heappop(dic_heap)
            term_dic.append(top_term)
            term_row = []
            for i in range(len(block_dic)):
                if dic_point[i] >= len(block_dic[i]):
                    continue
                if block_dic[i][dic_point[i]] != top_term:
                    continue
                temp_block_row = block_doc_csv[i].next()
                for x in temp_block_row:
                    if int(x) in term_row:
                        continue
                    term_row.append(int(x))
                dic_point[i] += 1
            term_doc.append(term_row)
        return term_dic, term_doc

    def _build_index_block(self):
        """
        建立索引块
        :return:
        """
        index_block = 0
        while True:
            term_dic, term_cnt, inverted_index = self._spimi_invert()
            index_block += 1
            self._index_block_path.append(os.path.join(self._index_block_dir,
                                                       'block_' + str(index_block)))
            self._write_index_block(term_dic, inverted_index,
                                    self._index_block_path[-1])
            if self._stream_is_empty:
                break

    def _write_index_block(self, dictionary, inverted_index, index_block_path):
        """
        把索引块写入到瓷盘中暂存
        :param dictionary:
        :param inverted_index:
        :param index_block_path:
        :return:
        """
        dic_sorted = [(k, dictionary[k]) for k in sorted(dictionary.keys())]
        temp = [0] * len(dic_sorted)
        for i, (k, v) in enumerate(dic_sorted):
            temp[i] = inverted_index[v]
        Dictionary.write_dictionary([k for k, v in dic_sorted], index_block_path + '_dic')
        Gamma.write_inverted_index_decode(temp, index_block_path + '_doc')

    def get_statistic(self):
        return self._statistic

if __name__ == '__main__':
    file_dir = os.path.join(os.getcwd(), '../data/document')
    ind = Index(file_dir)
    ind.build_index()

