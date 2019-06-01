import socket
import threading
from src.hex2Ascii import Converter


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
    bind_ip = '192.168.100.102'
    bind_port = 7020

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(10)  # max backlog of connections
    newSocket, clientAddr = server.accept()
    print(newSocket)

    newSocket, clientAddr = server.accept()
    print('ok')
    print(unicode2hex_str(newSocket.recv(1024)))
    answer_data = '68 32 00 32 00 68 40 02 37 02 00 06 00 60 00 00 01 00 e2 16'
    newSocket.send(Converter.hex_array2bytes(answer_data))
    # print(unicode2hex_str(newSocket.recv(1024)))
    f1002 = '68 8a 00 8a 00 68 4b 02 37 02 00 06 0c 71 00 00 02 7d 14 00 70 70 61 30 30 38 65 67 73 2f 6c 61 63 6f 6c 2f 74 6e 6d 2f 9b 16'
    newSocket.send(Converter.hex_array2bytes(f1002))
    print(unicode2hex_str(newSocket.recv(2048)))
    while True:
        data = newSocket.recv(1024)
        sendData = ''
        newSocket.send(Converter.hex_array2bytes(sendData))
        print(unicode2hex_str(data))

    # print(recvData)
