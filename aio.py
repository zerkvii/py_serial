import serial
import asyncio
from src.hex2Ascii import Converter


class Output(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False
        transport.write(Converter.hex_array2bytes(
            '68 9e 00 9e 00 68 4b 02 37 02 00 06 0c 71 00 00 04 7d 13 00 68 73 2e 6b 63 65 68 63 2f 6c 61 63 6f 6c 2f 74 6e 6d 2f 00 00 00 00 e8 03 76 16'))

    def data_received(self, data):
        print('data received', repr(data))
        self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        asyncio.get_event_loop().stop()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = serial.aio.create_serial_connection(loop, Output, 'COM3', baudrate=9600)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
