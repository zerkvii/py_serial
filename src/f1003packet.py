import re

from src.hex2Ascii import Converter


class EPacket:
    __head = '68'
    __tail = '16'
    __stable_field = '4b 02 37 02 00 06 0c 71 00 00 04 7d'
    __path_len = ''
    __path = ''
    __offset_address = ''
    __req_data_length = ''
    __crc32 = ''
    __data_len_field = ''

    def __init__(self, hex_path: str, offset: int, req: int) -> None:
        # file path |2 bytes
        self.__path_len = EPacket.get_path_len_str(hex_path)
        # path_len |n bytes
        self.__path = hex_path
        # file data offset |4 bytes
        self.__offset_address = EPacket.get_reversed_offset(offset)
        # require data length |2 bytes
        self.__req_data_length = EPacket.get_reversed_packet_len(req)
        # 1 byte
        self.__crc32 = EPacket.get_crc32(EPacket.get_data_field(self))
        # 2 bytes
        self.__data_len_field = EPacket.get_data_len_field(EPacket.get_data_field(self))

    def get_data_field(self):
        return self.__stable_field + ' ' + self.__path_len + ' ' + self.__path + ' ' + self.__offset_address + ' ' + \
               self.__req_data_length

    def get_assemble_packet(self):
        return self.__head + 2 * (
                ' ' + self.__data_len_field) + ' ' + self.__head + ' ' + self.get_data_field() + ' ' + self.__crc32 + \
               ' ' + self.__tail
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
        """

        :param data:
        :return: hex len of data
        """
        bytes_len = len(data.split(' '))
        bin_shift_len = bin(bytes_len)[2:] + '10'
        hex_str = hex(int(bin_shift_len, 2))[2:]
        final_hex_str = hex_str.rjust(4, '0')
        fhs_array = re.findall('.{2}', final_hex_str)
        return ' '.join(fhs_array[::-1])

    @staticmethod
    def get_reversed_offset(val: int) -> str:
        """

        :param val:
        :return:reversed hex str of offset
        """
        hex_str = hex(val)[2:]
        final_hex_str = hex_str.rjust(8, '0')
        fhs_array = re.findall('.{2}', final_hex_str)
        return ' '.join(fhs_array[::-1])

    @staticmethod
    def get_reversed_packet_len(val: int) -> str:
        """

        :param val:
        :return: reversed hex str of packet len
        """
        hex_str = hex(val)[2:]
        final_hex_str = hex_str.rjust(4, '0')
        fhs_array = re.findall('.{2}', final_hex_str)
        return ' '.join(fhs_array[::-1])


if __name__ == '__main__':
    # 实例化类
    test = EPacket(Converter.str2reversed_space_hex('/mnt/local/sge800app'), 0, 1000)
    print(test.get_data_field())
    print(test.get_assemble_packet())
    # packet = EPacket(Converter.str2reversed_space_hex('/mnt/local/start.sh'))
    # print(packet.get_assemble_packet())
