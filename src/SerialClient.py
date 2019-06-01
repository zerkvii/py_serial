import serial
from src.hex2Ascii import Converter
from src.f1002packet import FPacket
from src.f1003packet import EPacket
import re
import time


class SerialClient:
    f1002_received_data = ''

    def __init__(self, filename: str, ser: serial.Serial):
        self.ser = ser

        self.filename = filename
        self.f1002_packet = SerialClient.construct_f1002(filename)
        _, self.file_size = self.get_f1002_received_data()
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

    def get_f1002_received_data(self) -> (str, int):
        """

        :return:f1002 respond packet
        """
        try:
            # 写数据
            result = self.ser.write(Converter.hex_array2bytes(self.f1002_packet))
            print("写总字节数:", result)

        except Exception as e:
            print("---异常---：", e)
        trans_data = ''

        while True:
            num = 0
            try:
                num = self.ser.inWaiting()
            except Exception as e:
                print(e)
            if num > 0:
                print(num)
                data = self.ser.read(num)
                for i in range(0, len(data)):
                    tmp_data = '{:02X}'.format(data[i])
                    trans_data = trans_data + tmp_data
                    if tmp_data == '16':
                        leng = Converter.reversed_hex2int(trans_data[-34:-26])
                        return trans_data, leng

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
        all_count = 0
        while left_data_size > 0:
            if 0 < left_data_size <= 1000:
                epacket = SerialClient.construct_f1003(self.filename, offset_, left_data_size)
                left_data_size -= left_data_size
            else:
                epacket = SerialClient.construct_f1003(self.filename, offset_, 1000)
                offset_ += 1000
                left_data_size -= 1000
            try:
                # 写数据
                result = self.ser.write(Converter.hex_array2bytes(epacket.get_assemble_packet()))
                print(epacket.get_assemble_packet())
                print("写总字节数:", result)
            except Exception as e:
                print("---异常---：", e)
            trans_data = ''

            FLAG = True
            sleep_flag = True
            while FLAG:
                if sleep_flag:
                    time.sleep(1)
                    sleep_flag = False
                try:
                    num = self.ser.inWaiting()
                except Exception as e:
                    FLAG = False
                    print(e)
                if num > 0:
                    print('num', num)
                    data = self.ser.read(num)
                    for i in range(0, len(data)):
                        tmp_data = '{:02X}'.format(data[i])
                        trans_data = trans_data + tmp_data
                if num == 0:
                    all_count += len(trans_data[48:-4])
                    data_serial = re.findall('.{2}', trans_data[48:-4])[::-1]
                    final_data = ''.join(data_serial)
                    print(' '.join(data_serial))
                    f = open('append.txt', 'a+')
                    f.write(final_data)
                    f.close()
                    FLAG = False
                # if num > 0:
                #     this_count+=num
                #     data = self.ser.read(num)
                #     for i in range(0, len(data)):
                #         tmp_data = '{:02X}'.format(data[i])
                #         trans_data = trans_data + tmp_data
                #         if tmp_data == '16':
                #             print(trans_data,this_count)
                #             all_count += len(trans_data[48:-4])
                #             data_serial = re.findall('.{2}', trans_data[48:-4])[::-1]
                #             final_data = ''.join(data_serial)
                #             f = open('append.txt', 'a+')
                #             f.write(final_data)
                #             f.close()
                #             FLAG = False
            print(all_count, left_data_size, 'result')
            # break


if __name__ == '__main__':
    try:
        # 端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
        portx = "COM3"
        # 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
        bps = 9600
        # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
        timex = 0
        # 打开串口，并得到串口对象
        ser = serial.Serial(portx, bps, timeout=timex)
        ser.parity = 'E'
    except Exception as e:
        print(e)
    #
    sc = SerialClient('/mnt/local/sge800app', ser)
    sc.file_receive()
