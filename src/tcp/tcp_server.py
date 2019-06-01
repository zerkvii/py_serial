import socket
from src.hex2Ascii import Converter
from src.f1002packet import FPacket
from src.f1003packet import EPacket
import re
import time


class TcpServer:
    f1002_received_data = ''

    def __init__(self, filename: str, server: socket.socket, temp_file: str, req_data_len: int):
        self.server = server
        self.req_data_len = req_data_len
        self.temp_file = temp_file + '.txt'
        self.filename = filename
        self.f1002_packet = TcpServer.construct_f1002(filename)
        _, self.file_size = self.get_f1002_received_data()
        print(self.filename)
        # self.offset = 0
        # self.left_data_size = self.file_size
        self.file_data = ''

    @staticmethod
    def construct_f1002(filename: str) -> str:
        """

        :param filename:
        :return:hex f1002 packet of file
        """
        return FPacket(Converter.str2reversed_space_hex(filename)).get_assemble_packet()

    def answer(self):
        """
        the answer procedure
        :return:
        """
        try:
            self.server.recv(1024)
            answer_data = '68 32 00 32 00 68 40 02 37 02 00 06 00 60 00 00 01 00 e2 16'
            self.server.send(Converter.hex_array2bytes(answer_data))
        except Exception as e:
            print(e)

    def get_f1002_received_data(self) -> (str, int):
        """

        :return:f1002 respond packet
        """
        try:
            #
            self.server.send(Converter.hex_array2bytes(self.f1002_packet))
            f1002_received_data = self.server.recv(1024)
            print("f1002字节数:", len(f1002_received_data))
            trans_data = Converter.unicode2hex_str(f1002_received_data)
            leng = Converter.reversed_hex2int(trans_data[-34:-26])
            print(trans_data, leng)
            return trans_data, leng
        except Exception as e:
            print("---异常---：", e)

    @staticmethod
    def construct_f1003(filename: str, offset: int, packet_size: int) -> EPacket:
        """
        :return:EPacket
        """

        return EPacket(Converter.str2reversed_space_hex(filename), offset, packet_size)

    def file_receive(self) -> None:
        """
        this is to send f1003 packet to get file data
        append packet file data to instance filed ata filed
        :return:
        """
        offset_ = 0
        print(self.file_size)
        left_data_size = self.file_size
        rec_count = 0
        global_data = ''
        f1003_received_data = ''
        print('当前接收字节数：' + str(rec_count // 2), '剩余数据字节数：' + str(left_data_size))
        # rec_len = 0
        while left_data_size > 0:
            if 0 < left_data_size <= self.req_data_len:
                epacket = TcpServer.construct_f1003(self.filename, offset_, left_data_size)
                left_data_size -= left_data_size
            else:
                epacket = TcpServer.construct_f1003(self.filename, offset_, self.req_data_len)
                offset_ += self.req_data_len
                left_data_size -= self.req_data_len
            try:
                # 写数据
                self.server.send(Converter.hex_array2bytes(epacket.get_assemble_packet()))
                # result = self.s.write(Converter.hex_array2bytes(epacket.get_assemble_packet()))
                print(epacket.get_assemble_packet())
                f1003_received_data = self.server.recv(self.req_data_len * 2)
            except Exception as e:
                print("---异常---：", e)
            trans_data = Converter.unicode2hex_str(f1003_received_data)
            print("f1003接收数据包字节数:", len(trans_data) // 2)

            data_serial = re.findall('.{2}', trans_data[48:-4])[::-1]
            rec_count += len(data_serial)
            final_data = ''.join(data_serial)
            global_data += final_data
            print(len(global_data), 'global_data_len')
            print(' '.join(data_serial))

            print('当前接收字节数：' + str(rec_count), '剩余数据字节数：' + str(left_data_size))
        f = open(self.temp_file, 'w+')
        f.write(global_data)
        f.close()


if __name__ == '__main__':
    try:
        bind_ip = '192.168.127.10'
        bind_port = 8888

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((bind_ip, bind_port))
        server.listen(10)  # max backlog of connections
        newSocket, clientAddr = server.accept()
    except Exception as e:
        print(e)
    #
    sc = TcpServer('/mnt/local/local.sh', newSocket, 'local-sh', 1000)
    sc.file_receive()
    sc1 = TcpServer('/mnt/local/module.con', newSocket, 'module-con', 1000)
    sc1.file_receive()
