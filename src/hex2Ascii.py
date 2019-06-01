import binascii
import binhex
from typing import List
import re


class Converter:
    def __init__(self, s: str):
        self.hex_str = Converter.str2hex(s)
        self.hex_rsh = Converter.str2reversed_space_hex(s)
        self.hex_str_len = len(self.hex_str)
        self.str_byte_len = self.hex_str_len // 2

    @staticmethod
    def str2hex(s: str) -> str:
        """
        :param s:
        :return:hex str
        """
        return bytes.hex(s.encode('utf-8'))

    @staticmethod
    def reversed_hex2int(s: str) -> int:
        """

        :param s:
        :return:int of reversed 8 hex str
        """
        hex_array = re.findall('.{2}', s)
        origin_hex_str = ''.join(hex_array[::-1])
        return int(origin_hex_str, 16)

    @staticmethod
    def str2reversed_space_hex(s: str) -> str:
        """

        :param s:
        :return: reversed hex string with space split
        """
        hex_str = Converter.str2hex(s)
        hex_list = re.findall('.{2}', hex_str)
        return ' '.join(hex_list[::-1])

    @staticmethod
    def hex_array2bytes(s: str) -> bytes:
        """

        :param s:
        :return:bytes of hex string array
        """
        str_array = s.strip().split(' ')
        int_list = [int(x, 16) for x in str_array]
        return bytes(int_list)

    @staticmethod
    def unicode2hex_str(data: bytes) -> str:
        """

        :param data: bytes
        :return: hex str
        """
        trans_data = ''
        for i in range(0, len(data)):
            tmp_data = '{:02X}'.format(data[i])
            trans_data = trans_data + tmp_data
        return trans_data


if __name__ == '__main__':
    print(Converter.reversed_hex2int('0B030000'))
    print(Converter.hex_array2bytes(
        '68 86 00 86 00 68 4b 02 37 02 00 06 0c 71 00 00 02 7d 13 00 68 73 2e 6b 63 65 68 63 2f 6c 61 63 6f 6c 2f 74 6e 6d 2f 89 16'))
