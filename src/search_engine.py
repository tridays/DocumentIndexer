__author__ = 'xp'

import re

from typing import List, Set, Tuple, Dict

from src.document import Document
from src.tokenizer import Tokenizer


class SearchEngine:

    def __init__(self, docs: List[Document], term_dic: List[Tuple[str, int, int]], r_indices: List[List[int]]):
        self.docs = docs
        self.term_map = {}  # type: Dict[str, int]
        for i, info in enumerate(term_dic):
            self.term_map[info[0]] = i
        self.term_dic = term_dic
        self.r_indices = r_indices

    def search(self, text):
        text = re.findall('\w+|\||&', text)
        words = list(filter(lambda x: len(x) > 0, text))

        word_num = len(words)
        if word_num == 1:
            index = self._search_word(words[0])
        elif word_num == 3:
            lret = self._search_word(words[0])
            rret = self._search_word(words[2])
            if words[1] == '&':
                index = lret.intersection(rret)
            elif words[1] == '|':
                index = lret.union(rret)
            else:
                raise ValueError('无法识别布尔逻辑运算符')
        else:
            raise ValueError('参数数量非法')

        fetched = [self.docs[i] for i in index]
        return fetched

    def _search_word(self, word) -> Set[int]:
        term_id = self.term_map.get(Tokenizer.normalize(word))
        if term_id is None:
            return set()
        term_info = self.term_dic[term_id]
        ri_offset = term_info[2]
        return set(self.r_indices[ri_offset])
