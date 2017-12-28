__author__ = 'xp'

import os
import os.path

from typing import List, Tuple, Dict, Optional

from src.binutils import uint_to_bytes, bytes_to_uint
from src.compression import Compression
from src.gamma_encoder import Gamma
from src.term_provider import TermProvider


class Indexer(object):

    def __init__(self, term_provider: TermProvider, block_dir: str, indices_dir: str, block_size=5000):
        self.stream = iter(term_provider)
        self.block_dir = block_dir
        self.indices_dir = indices_dir
        self.block_size = block_size

    def build_and_save(self):
        """
        构建倒排索引
        1. 构建索引块，并保存
        2. 合并索引块，并保存
        """
        next_block_id = 0
        while True:
            continuable, term_doc, r_indices = self._build_block(self.block_size)
            self._save_block(self.block_dir, next_block_id, term_doc, r_indices)
            next_block_id += 1
            if not continuable:
                break
        term_dic, r_indices = self._build_global(next_block_id)
        self._save_block(self.indices_dir, None, term_dic, r_indices)

    def _build_block(self, max_block_size: int) -> (bool, List[Tuple[str, int, int]], List[List[int]]):
        """
        构建索引块
        """
        next_term_id = 0
        term_map = {}  # type: Dict[str, int]
        r_indices = []  # type: List[List[int]]
        continuable = True
        cur_block_size = 0
        try:
            while cur_block_size < max_block_size:
                term, doc_id = next(self.stream)
                if term not in term_map:
                    term_map[term] = next_term_id
                    r_indices.append([doc_id])
                    next_term_id += 1
                else:
                    term_id = term_map[term]
                    r_index = r_indices[term_id]
                    if doc_id != r_index[-1]:
                        r_index.append(doc_id)
                cur_block_size += 1
        except StopIteration:
            continuable = False
        term_dic = []  # type: List[Tuple[str, int, int]]
        for term in sorted(term_map.keys()):
            term_id = term_map[term]
            r_index = r_indices[term_id]
            term_dic.append((term, len(r_index), term_id))
        return continuable, term_dic, r_indices

    @staticmethod
    def _get_dictionary_file_path(save_dir: str, block_id: int) -> str:
        filename = 'merged' if block_id is None else 'block_%d' % block_id
        return os.path.join(save_dir, '%s.dic' % filename)

    @staticmethod
    def _get_index_file_path(save_dir: str, block_id: int) -> str:
        filename = 'merged' if block_id is None else 'block_%d' % block_id
        return os.path.join(save_dir, '%s.idx' % filename)

    @staticmethod
    def _save_block(save_dir: str, block_id: Optional[int], term_dic: List[Tuple[str, int, int]], r_indices: List[List[int]]):
        """
        保存索引块到磁盘
        """
        with open(Indexer._get_dictionary_file_path(save_dir, block_id), 'wb') as f:
            zipped = Compression.zip(term_dic)
            f.write(zipped)

        with open(Indexer._get_index_file_path(save_dir, block_id), 'wb') as f:
            for r_index in r_indices:
                encoded = Gamma.encode_index(r_index)
                f.write(uint_to_bytes(len(encoded)))
                f.write(encoded)

        with open(Indexer._get_index_file_path(save_dir, block_id) + '.dec', 'w') as f:
            for r_index in r_indices:
                f.write(' '.join(map(str, r_index)))
                f.write('\n')

    @staticmethod
    def _read_block(save_dir: str, block_id: Optional[int]) -> (List[Tuple[str, int, int]], List[List[int]]):
        """
        从磁盘读取索引块
        """
        with open(Indexer._get_dictionary_file_path(save_dir, block_id), "rb") as f:
            term_dic = Compression.unzip(f.read())
        with open(Indexer._get_index_file_path(save_dir, block_id), 'rb') as f:
            r_indices = []
            while True:
                size = f.read(4)
                if len(size) == 0:
                    break
                size = bytes_to_uint(size)
                r_index = Gamma.decode_index(f.read(size))
                r_indices.append(r_index)
        return term_dic, r_indices

    def _build_global(self, block_num: int) -> (List[Tuple[str, int, int]], List[List[int]]):
        """
        合并索引块
        从磁盘读取各块，合并相同词项的倒排记录表
        """
        next_term_id = 0
        term_map = {}  # type: Dict[str, int]
        r_indices = []  # type: List[List[int]]

        def insert_to_index(term_index: List[int], new_doc_id: int) -> bool:
            """
            有序地插入目标位置
            """
            for i, doc_id in enumerate(term_index):
                if doc_id == new_doc_id:
                    return False
                if doc_id > new_doc_id:
                    term_index.insert(i, new_doc_id)
                    return True
            term_index.append(new_doc_id)
            return True

        for i in range(block_num):
            b_term_dic, b_r_indices = self._read_block(self.block_dir, i)
            for term, freq, offset in b_term_dic:
                r_index = b_r_indices[offset]
                if term not in term_map:
                    term_map[term] = next_term_id
                    r_indices.append(r_index)
                    next_term_id += 1
                else:
                    term_id = term_map[term]
                    term_index = r_indices[term_id]
                    for doc_id in r_index:
                        insert_to_index(term_index, doc_id)

        term_dic = []  # type: List[Tuple[str, int, int]]
        for term in sorted(term_map.keys()):
            term_id = term_map[term]
            r_index = r_indices[term_id]
            term_dic.append((term, len(r_index), term_id))
        return term_dic, r_indices

    def read_global_block(self) -> (List[Tuple[str, int, int]], List[List[int]]):
        return self._read_block(self.indices_dir, None)


if __name__ == '__main__':
    term_provider1 = TermProvider('../assets/trecs', '../assets/index/stop_words')
    indexer1 = Indexer(term_provider1, '../assets/blocks', '../assets/index')
    indexer1.build_and_save()
