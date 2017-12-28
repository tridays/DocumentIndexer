__author__ = 'xp'


def uint_to_bytes(v: int) -> bytes:
    return v.to_bytes(4, byteorder='little', signed=False)


def bytes_to_uint(v: bytes) -> int:
    return int.from_bytes(v, byteorder='little', signed=False)
