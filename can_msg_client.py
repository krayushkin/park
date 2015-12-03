# test client for tcp/uart server
# recieve messages from localhost:2000 and display it

import asyncio
import struct
import sys



class MsgGenClient(asyncio.Protocol):
    def connection_made(self, transport):
        print("Connected")
        self.is_closed = False
        self.transport = transport

    def data_received(self, data):
        print(data)
  
    def connection_lost(self, exc):
        print("Connection lost")
        self.transport.close()
        self.is_closed = True


loop = asyncio.get_event_loop()
coro = loop.create_connection(MsgGenClient, 'localhost', 2000)
server = asyncio.async(coro)


try:
    loop.run_forever()
except KeyboardInterrupt:
    print("exit")
finally:
    loop.close()

