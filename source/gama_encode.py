# -*- coding: utf-8 -*-
__author__ = 'zhsl'
import os
import csv
import struct


class Gamma:

    def __init__(self):
        return

    @staticmethod
    def encode(num):
        """
        对一个数字进行 Gamma 压缩, 对数字进行偏移一位的操作
        对于一个数 num, 其对应的 Gamma 的编码为 Gamma(num + 1)
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
        """
        对倒排索引进行 Gamma 加密
        :param inverted_index: ex. [[1, 2, 3], [3, 4]]
        :return:
        """
        ret = []
        for row in inverted_index:
            s = Gamma.encode(row[0])
            for i, x in enumerate(row[1:]):
                s += Gamma.encode(x - row[i])
            ret.append(s)
        return ret

    @staticmethod
    def decode(code):
        """
        对一个 Gamma 编码进行解密
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
    def decode_inverted_index(encode_index):
        """
        对倒排索引中的一个 Gamma 压缩的倒排记录进行解密
        Gamma 压缩的倒排记录第一个数是文档ID, 其后的数子为文档ID间隔
        返回词项对应的每个文档ID
        :param encoode_index: ex. '101101101101010110100000'
        :return:
        """
        ret = []
        row = []
        num_len = i = flag = pre = 0
        while i < len(encode_index):
            if encode_index[i] == '0' and len(row) != 0:
                ret.append(row)
                row = []
                i += 1
                flag = pre = 0
            while encode_index[i + num_len] == '1':
                num_len += 1
            if num_len > 0:
                num = Gamma.decode(encode_index[i:i+1+num_len+num_len])
                if flag == 0:
                    flag = 1
                row.append(pre + num)
                pre += num
            i += 1 + num_len + num_len
            num_len = 0
        return ret

    @staticmethod
    def reade_inverted_index_encode(file_path):
        """
        读取 Gamma 编码的倒排索引, 从磁盘中读取压缩的倒排记录表,
        并通过 decode_inverted_index() 函数返回解压后的倒排记录表
        :param inverted_index:
        :param dic_sorted:
        :param file_path:
        :return:
        """
        ret = []
        with open(file_path, 'rb') as reader_file:
            row = ''
            while True:
                x = reader_file.read(4)
                x = struct.unpack('i', x)[0]
                if x is 0:
                    break
                i = 0
                while i < 31:
                    row += '1' if x & (1 << i) else '0'
                    i += 1
        return Gamma.decode_inverted_index(row)

    @staticmethod
    def write_inverted_index_decode(inverted_index, file_path):
        """
        把未压缩的倒排记录表写入到瓷盘中
        :param inverted_index:
        :param file_path:
        :return:
        """
        with open(file_path, 'w') as write_file:
            writer = csv.writer(write_file, delimiter=' ')
            writer.writerows(inverted_index)

    @staticmethod
    def write_inverted_index_encode(inverted_index, file_path):
        """
        把压缩好的倒排记录表写入磁盘中
        :param inverted_index:
        :param dic_sorted:
        :param file_path:
        :return:
        """
        with open(file_path, 'wb') as write_file:
            inverted_index_encode = Gamma.encode_inverted_index(inverted_index)
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
            if k != 0:
                write_file.write(struct.pack('i', temp))
            write_file.write(struct.pack('i', 0))

if __name__ == '__main__':
    print Gamma.encode(2)
    print Gamma.encode(4)
    print Gamma.decode('101')
    print Gamma.decode('11001')
    # [['100100101'], ['1011010000']]
    print Gamma.encode_inverted_index([[1, 2, 4], [2, 4]])
    # [[1, 2, 4], [2, 4]]
    print Gamma.decode_inverted_index('1001001010101101000000')
    file_dir = os.path.join(os.getcwd(), '../data/index/doc_index_encode')
    inverted_index = Gamma.reade_inverted_index_encode(file_dir)
    print len(inverted_index), inverted_index
