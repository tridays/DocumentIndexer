__author__ = 'xp'

import re

from typing import List, Tuple, Iterable, Generator

from .document import Document


class Tokenizer(object):
    def __init__(self, stopwords: Iterable[str]):
        self.stopwords = set(map(self.normalize, stopwords))

    @staticmethod
    def normalize(word: str) -> str:
        """
        对词条归一化
        """
        return word.strip().lower()

    def is_stopword(self, word: str) -> bool:
        """
        判断停用词
        """
        return word in self.stopwords

    def iter_tokens(self, doc: Document) -> Generator[str, None, None]:
        """
        获取词条，去停用词，统一大小写
        """
        raw = re.findall('\w+', doc.body)
        doc.token_nums = len(raw)
        for token in raw:
            token = self.normalize(token)
            if not self.is_stopword(token):
                yield token

    def iter_terms(self, docs: List[Document]) -> Generator[Tuple[str, int], None, None]:
        """
        获取词项
        """
        for index, doc in enumerate(docs):
            tokens = self.iter_tokens(doc)
            for token in tokens:
                doc.term_nums += 1
                yield (token, index)
