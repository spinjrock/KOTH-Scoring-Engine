#A very basic idea for the scoring engine

#Imports
import queue
import socket
import asyncio
import json

#Constant Declarations
HOST_IP = socket.gethostbyname(socket.gethostname())
LOOPBACK_IP = "127.0.0.1"
RECV_UDP_PORT = 50435
DATAGRAM_SIZE = 2048
ACTIVE_IP = LOOPBACK_IP
MAGIC_BYTES = b"\x13\x90"

#Globals

async def send_message():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    json_message = json.dumps({"test": "key"}).encode()
    message = MAGIC_BYTES + json_message
    print(message)
    sock.sendto(message, (ACTIVE_IP, RECV_UDP_PORT))

async def main():
    while True:
        await asyncio.gather(send_message())
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())