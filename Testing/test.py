#A very basic idea for the scoring engine

#Imports
import queue
import socket
import asyncio

#Constant Declarations
HOST_IP = socket.gethostbyname(socket.gethostname())
LOOPBACK_IP = "127.0.0.1"
RECV_UDP_PORT = 50435
DATAGRAM_SIZE = 2048
ACTIVE_IP = LOOPBACK_IP
MAGIC_BYTES = b"\x13\x90"

#Globals
Incoming_Message_Queue = queue.Queue()

async def recv_message():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ACTIVE_IP, RECV_UDP_PORT))
    raw_message, client = sock.recvfrom(DATAGRAM_SIZE)
    if raw_message[0:2] == MAGIC_BYTES:
        Incoming_Message_Queue.put(raw_message[2:])
    else:
        return
    

async def process_messages():
    while Incoming_Message_Queue.qsize() > 0:
        print(Incoming_Message_Queue.get().decode())

async def main():
    while True:
        await asyncio.gather(process_messages(), recv_message())

if __name__ == "__main__":
    asyncio.run(main())