__author__ = 'xp'

from typing import Iterator, List


class Gamma(object):

    @staticmethod
    def _encode(num: int) -> str:
        b_str = bin(num)[3:]
        return '1' * len(b_str) + '0' + b_str

    @staticmethod
    def encode(nums: Iterator[int]) -> bytearray:
        """
        Gamma 编码，byte 对齐时补 1
        """
        s = ''.join(map(Gamma._encode, nums))
        padding = 8 - len(s) % 8
        if padding > 0:
            s += '1' * padding
        s_len = len(s)
        b = bytearray(s_len // 8)
        s_pos = 0
        b_pos = 0
        while s_pos < s_len:
            b[b_pos] = int(s[s_pos:s_pos+8], 2)
            s_pos += 8
            b_pos += 1
        return b

    @staticmethod
    def decode(encoded: bytes) -> Iterator[int]:
        """
        Gamma 解码
        """
        b_pos = 0
        b_len = len(encoded)
        scan_unary = True
        off_len = 0
        off_str = None
        while b_pos < b_len:
            byte = encoded[b_pos]
            pivot = 0x80
            while pivot != 0:
                if scan_unary:
                    if byte & pivot == 0:
                        if off_len == 0:
                            yield 1
                        else:
                            scan_unary = False
                            off_str = ''
                    else:
                        off_len += 1
                else:
                    off_str += str(0 if byte & pivot == 0 else 1)
                    off_len -= 1
                    if off_len == 0:
                        yield int('1' + off_str, 2)
                        scan_unary = True
                pivot >>= 1
            b_pos += 1
        if not scan_unary:
            if off_len == 0:
                yield int('1' + off_str, 2)
            else:
                raise EOFError("unexpected eof")

    @staticmethod
    def encode_index(index: List[int]) -> bytearray:
        """
        对索引编码，将 doc_id 算为偏移量
        """
        last = 0
        offs = []
        for doc_id in index:
            if doc_id < last:
                raise ValueError("unsorted index")
            offs.append(doc_id - last)
            last = doc_id
        return Gamma.encode(offs)

    @staticmethod
    def decode_index(encoded: bytes) -> List[int]:
        """
        对索引解码，将偏移量转为 doc_id
        """
        index = []
        sum = 0
        for offset in Gamma.decode(encoded):
            sum += offset
            index.append(sum)
        return index


if __name__ == '__main__':
    assert Gamma.encode([5]) == bytearray([207])
    i = next(Gamma.decode(Gamma.encode([2])))
    assert i == 2

    assert Gamma.encode_index([1, 2, 4]) == bytearray([39])

    indices1 = [1, 2, 4, 8, 9]
    assert Gamma.decode_index(Gamma.encode_index(indices1)) == indices1
