# can message generator
# send can messages over tcp every 1 sec on address localhost:1234

import asyncio
import struct
import sys

def message_helper(b):
    for byte in b:
        yield (int(byte) >> 0) & 0x0F
        yield (int(byte) >> 4) & 0x0F


def message(std_id, data):
    dlc = len(data)
    assert 1 <= dlc <= 8
    return struct.pack("17B{0}B".format(dlc*2), 
            0xf0, # start byte
            0x00, # RESERVED1
            (std_id >>  0) & 0x0F, # STD_ID
            (std_id >>  4) & 0x0F,
            (std_id >>  8) & 0x0F,
            (std_id >> 12) & 0x0F,
            0x00, # RESERVED2
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
            dlc & 0x0F, 
            *message_helper(data)
            )

@asyncio.coroutine
def send_message(protocol):
    i = 0
    if not protocol.is_closed:
        protocol.transport.write(b"test\r\n")
        ++i
        yield from asyncio.sleep(1)
        yield from send_message(protocol)


class MsgGenClient(asyncio.Protocol):
    def connection_made(self, transport):
        self.is_closed = False
        self.transport = transport
        asyncio.async(send_message(self))


    def connection_lost(self, exc):
        print("Connection lost")
        self.transport.close()
        self.is_closed = True


loop = asyncio.get_event_loop()
coro = loop.create_connection(MsgGenClient, '127.0.0.1', 1234)
server = asyncio.async(coro)


try:
    loop.run_forever()
except KeyboardInterrupt:
    print("exit")
finally:
    server.close()
    loop.close()

