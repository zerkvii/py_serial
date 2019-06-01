import re

from src.hex2Ascii import Converter


class FPacket:
    __head = '68'
    __tail = '16'
    __stable_field = '4b 02 37 02 00 06 0c 71 00 00 02 7d'
    __path_len = ''
    __path = ''
    __crc32 = ''
    __data_len_field = ''

    def __init__(self, hex_path: str) -> None:
        # self.__head = '68'
        # 2 bytes
        self.__path_len = FPacket.get_path_len_str(hex_path)
        # path_len bytes
        self.__path = hex_path
        # 1 byte
        self.__crc32 = FPacket.get_crc32(FPacket.get_data_field(self))
        # 2 bytes
        self.__data_len_field = FPacket.get_data_len_field(FPacket.get_data_field(self))
        # self.__tail = '16'

    def get_data_field(self):
        return self.__stable_field + ' ' + self.__path_len + ' ' + self.__path

    def get_assemble_packet(self):
        return self.__head + 2 * (
                ' ' + self.__data_len_field) + ' ' + self.__head + ' ' + self.get_data_field() + ' ' + self.__crc32 + ' ' + self.__tail
        # return self._tail+2*(' '+self

    @staticmethod
    def get_path_len_str(s: str) -> str:
        """

        :param s:
        :return: using reversed hex to express bytes of file path str
        """
        bytes_len = len(s.split(' '))
        hex_str = str(hex(bytes_len))[2:]
        final_hex_str = hex_str.rjust(4, '0')
        fhs_array = re.findall('.{2}', final_hex_str)
        return ' '.join(fhs_array[::-1])

    @staticmethod
    def get_crc32(s: str) -> str:
        """

        :param s:
        :return:hex str of crc
        """
        s_list = s.split(' ')
        hex_list = [int('0x' + x, 16) for x in s_list]
        return str(hex(sum(hex_list)))[-2:]

    @staticmethod
    def get_data_len_field(data: str) -> str:
        bytes_len = len(data.split(' '))
        bin_shift_len = bin(bytes_len)[2:] + '10'
        hex_str = hex(int(bin_shift_len, 2))[2:]
        final_hex_str = hex_str.rjust(4, '0')
        fhs_array = re.findall('.{2}', final_hex_str)
        return ' '.join(fhs_array[::-1])


if __name__ == '__main__':
    # 实例化类
    packet = FPacket(Converter.str2reversed_space_hex('/mnt/local/version.inf'))
    print(packet.get_assemble_packet())
