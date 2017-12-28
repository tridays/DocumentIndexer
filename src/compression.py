__author__ = 'xp'

from typing import List, Tuple, Dict

from src.binutils import uint_to_bytes, bytes_to_uint


class Compression(object):

    @staticmethod
    def zip(dic: List[Tuple[str, int, int]]) -> bytes:
        """
        压缩词典为单一字符串
        :param dic: [(term, freq, pi_offset)]
        :return:
        """
        s = b''
        for item in dic:
            term_b = bytes(item[0], encoding='utf-8')
            s += uint_to_bytes(len(term_b)) \
                 + term_b \
                 + uint_to_bytes(item[1]) \
                 + uint_to_bytes(item[2])
        return s

    @staticmethod
    def unzip(zipped: bytes) -> List[Tuple[str, int, int]]:
        """
        从单一字符串解压缩词典
        :param zipped:
        :return: [(term, freq, pi_offset)]
        """
        dic = []  # type: List[Tuple[str, int, int]]
        size = len(zipped)
        p = 0
        while p < size:
            term_len = bytes_to_uint(zipped[p:p + 4])
            p += 4
            term = str(zipped[p:p + term_len], encoding='utf-8')
            p += term_len
            freq = bytes_to_uint(zipped[p:p + 4])
            p += 4
            pi_offset = bytes_to_uint(zipped[p:p + 4])
            p += 4
            dic.append((term, freq, pi_offset))
        return dic

    @staticmethod
    def dict2list(dic: Dict[str, Tuple[int, int]]) -> List[Tuple[str, int, int]]:
        sorted_dic = []  # type: List[Tuple[str, int, int]]
        for k in sorted(dic.keys()):
            v = dic[k]
            sorted_dic = (k, v[0], v[1])
        return sorted_dic

    @staticmethod
    def list2dict(sorted_dic: List[Tuple[str, int, int]]) -> Dict[str, Tuple[int, int]]:
        dic = {}  # type: Dict[str, Tuple[int, int]]
        for item in sorted_dic:
            dic[item[0]] = (item[1], item[2])
        return dic


if __name__ == '__main__':
    dic1 = [('hello', 3, 0)]
    assert Compression.zip(dic1) == b'\x05\x00\x00\x00hello\x03\x00\x00\x00\x00\x00\x00\x00'
    assert Compression.unzip(Compression.zip(dic1)) == dic1
