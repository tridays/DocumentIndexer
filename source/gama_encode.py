# -*- coding: utf-8 -*-
__author__ = 'zhsl'
import csv


class Gama:

    def __init__(self):
        return

    @staticmethod
    def encode(num):
        """
        3 -> 11 -> 10, 1 -> 101
        5 -> 101 -> 110, 01 -> 11001
        :param num:
        :return:
        """
        num += 1
        i = 31
        while not (num & (1 << i)):
            i -= 1
        ret = '1' * i + '0'
        i -= 1
        while i >= 0:
            ret += '1' if num & (1 << i) else '0'
            i -= 1
        return ret

    @staticmethod
    def encode_inverted_index(inverted_index):
        ret = []
        for row in inverted_index:
            s = Gama.encode(row[0])
            for i, x in enumerate(row[1:]):
                s += Gama.encode(x - row[i])
            ret.append(s)
        return ret

    @staticmethod
    def decode(code):
        """
        101 -> 10, 1 -> 11 -> 3
        11001 -> 110, 01 -> 101 -> 5
        :param code:
        :return:
        """
        code_len = len(code)
        i = 0
        while code[i] == '1':
            i += 1
        ret = 1 << i
        while i > 0:
            w = code_len - i
            i -= 1
            ret |= 1 << i if code[w] == '1' else 0
        return ret - 1

    @staticmethod
    def decode_inverted_index(encoode_index):
        ret = []
        for k, row in enumerate(encoode_index):
            ret.append([])
            len_row = len(row)
            i = 0
            while i < len_row:
                start = i
                code_len = 0
                if row[i] == '1':
                    code_len += 1
                end = start + code_len + 1 + code_len
                num = Gama.decode(row[start:end])
                if len(ret[k]) == 0:
                    ret[k].append(num)
                else:
                    ret[k].append(num + ret[k][-1])
                i = end
        return ret

if __name__ == '__main__':
    print Gama.encode(2)
    print Gama.encode(4)
    print Gama.decode('101')
    print Gama.decode('11001')
    print Gama.encode_inverted_index([[2, 4], [2, 4]])
    print Gama.decode_inverted_index(['101101', '101101'])
