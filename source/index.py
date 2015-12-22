# -*- coding: utf-8 -*-
__author__ = 'zhsl'
import os
import csv
import struct
from stream import TokenStream
from gama_encode import Gama


class Index:

    def __init__(self, document_path, max_block=5000):
        self._dir_path = os.path.dirname(document_path)
        self._index_block_dir = os.path.join(self._dir_path, 'index_block')
        self._index_block_path = []
        self._token_stream = TokenStream(document_path)
        self._stream_is_empty = False
        self._term_dic = {}
        self._term_cnt = 0
        self._inverted_index = []
        self._max_block = max_block
        return

    def _spimi_invert(self):
        """
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
        构建索引
        :return:
        """
        index_block = 0
        # 构建索引块
        while True:
            term_dic, term_cnt, inverted_index = self._spimi_invert()
            index_block += 1
            self._index_block_path.append(os.path.join(self._index_block_dir,
                                                       'block_' + str(index_block)))
            self._write_index_block(term_dic, inverted_index,
                                    self._index_block_path[-1])
            if self._stream_is_empty:
                break
        # 合并每个索引块, 构建全局索引

        return

    def _write_index_block(self, dictionary, inverted_index, index_block_path):
        dic_sorted = [(k, dictionary[k]) for k in sorted(dictionary.keys())]
        temp = [0] * len(dic_sorted)
        for i, (k, v) in enumerate(dic_sorted):
            temp[i] = inverted_index[v]
        self._write_inverted_index_encode(temp, [k for k, v in dic_sorted],
                                          index_block_path)

    def _write_inverted_index_decode(self, inverted_index, dic_sorted,
                                     file_path):
        dic_compression = self._compression_dictionary(dic_sorted)
        with open(file_path, 'w') as write_file:
            write_file.writelines(dic_compression)
        with open(file_path, 'a+') as write_file:
            writer = csv.writer(write_file, delimiter=' ')
            writer.writerows(inverted_index)

    def _write_inverted_index_encode(self, inverted_index, dic_sorted,
                                     file_path):
        """
        写入 Gama 编码的 inverted_index
        :param inverted_index:
        :param dic_sorted:
        :param file_path:
        :return:
        """
        dic_compression = self._compression_dictionary(dic_sorted)
        with open(file_path, 'wb') as write_file:
            write_file.writelines(dic_compression)
            inverted_index_encode = Gama.encode_inverted_index(inverted_index)
            temp = k = 0
            for row in inverted_index_encode:
                for x in row:
                    temp |= (1 << k) if x == '1' else 0
                    k += 1
                    if k == 31:
                        write_file.write(struct.pack('i', temp))
                        temp = k = 0
                k += 1
                if k == 31:
                    write_file.write(struct.pack('i', temp))
                    temp = k = 0

    def _compression_dictionary(self, dic_sorted):
        """
        压缩词典
        :param dic_sorted:
        :return:
        """
        ret = ''
        for term in dic_sorted:
            ret += str(len(term))
            ret += term
        return ret

    def get_term_dic(self):
        return self._term_dic

    def get_inverted_index(self):
        return self._inverted_index

if __name__ == '__main__':
    file_dir = os.path.join(os.getcwd(), '../data/document')
    ind = Index(file_dir)
    ind.build_index()

