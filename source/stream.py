# -*- coding: utf-8 -*-
__author__ = 'zhsl'
import os
import bs4
from token_process import Token
import re
import json

class TokenStream:

    def __init__(self, file_dir):
        """
        读取文档文件, 得到对应的 term - document_id
        :param file_dir: document's path
        :return:
        """
        self._file_dir = file_dir
        self._file_names = os.listdir(self._file_dir)
        self._document = None
        self._document_id = 0
        self._document_term = []
        self._document_num = {}
        self._term_position = -1
        self._token = Token()

    def _next_file_path(self):
        """
        获取下一个文档文件的路径
        :return:
        """
        if len(self._file_names) is 0:
            return None
        file_path = os.path.join(self._file_dir, self._file_names[0])
        self._file_names.pop(0)
        return file_path

    def _next_document(self):
        """
        从 /data/document/ 下的一个文件获取一篇文档,
        通过 Beautiful Soup 解析 html
        :return:
        """
        if type(self._document) is bs4.element.Tag:
            self._document = self._document.next_sibling
        while type(self._document) is not bs4.element.Tag:
            if self._document is None:
                file_path = self._next_file_path()
                if file_path is None:
                    return None
                with open(file_path, 'r') as document_file:
                    soup = bs4.BeautifulSoup(document_file, features='lxml')
                self._document = soup.doc
            else:
                self._document = self._document.next_sibling

    def _get_document_term(self):
        """
        从 self._cocument 获取文档的每个词项
        :return:
        """
        self._next_document()
        if self._document is None:
            self._document_term = None
            return None
        self._document_id += 1
        docno_name = self._document.docno.string
        self._document_num[self._document_id] = docno_name
        temp = ''
        for row in self._document.docno.next_siblings:
            if type(row) is bs4.element.Tag:
                row = row.strings
            if type(row) is not bs4.element.NavigableString:
                continue
            temp += row.lower().encode('utf-8')
        self._term_position = -1
        self._document_term = self._token.get_term(re.findall(r'\w+', temp))

    def _next_term(self):
        """
        去读下个词项以及词项在文档中的位置
        :return:
        """
        self._term_position += 1
        while self._term_position >= len(self._document_term):
            self._get_document_term()
            self._term_position += 1
            if self._document_term is None:
                return None
        return self._document_term[self._term_position]

    def next_term_docid(self):
        """
        获取下一个 词项, 词项位置, 文档ID
        :return:
        """
        ret = self._next_term()
        if ret is None:
            return None
        return (ret[0], ret[1], self._document_id)

    def ouput_document_num(self, file_path):
        file_path = os.path.join(file_path, 'document_num')
        with open(file_path, 'w') as writer_file:
            writer_file.write(json.dumps(self._document_num))


if __name__ == '__main__':
    file_dir = os.getcwd() + '/../data/document'
    di = TokenStream(file_dir)
    while (di.is_empty() is False):
        print di.is_empty()
        ret = di.next_term_docid()
        print ret

