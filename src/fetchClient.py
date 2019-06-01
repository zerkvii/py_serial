import serial
from src.hex2Ascii import Converter
import time

if __name__ == '__main__':
    ser = None
    try:
        # 端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
        portx = "COM3"
        # 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
        bps = 9600
        # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
        timex = 60
        # 打开串口，并得到串口对象
        ser = serial.Serial(portx, bps,timeout=timex)
        ser.parity = 'E'
    except Exception as e:
        print(e)
    try:
        # 写数据
        result = ser.write(Converter.hex_array2bytes(
            '68 9e 00 9e 00 68 4b 02 37 02 00 06 0c 71 00 00 04 7d 13 00 68 73 2e 6b 63 65 68 63 2f 6c 61 63 6f 6c 2f 74 6e 6d 2f 00 00 00 00 e8 03 76 16'))
        print("写总字节数:", result)

    except Exception as e:
        print("---异常---：", e)
    trans_data = ''

    while True:
        num = 0
        try:
            num = ser.inWaiting()
        except Exception as e:
            print(e)
        count = 0
        if num > 0:
            print(num)

            data = ser.read(num)
            for i in range(0, len(data)):
                tmp_data = '{:02X}'.format(data[i])
                if tmp_data == '16':
                    count += 1
                trans_data = trans_data + tmp_data
            print(len(trans_data), trans_data)
            if count >= 0:
                print('count:' + str(count))
            # break
            # num = len(data)
            # # hex显示
