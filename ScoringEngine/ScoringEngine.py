#A very basic idea for the scoring engine

#Imports
import queue
import socket
import json

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
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                         #Initialize Socket
    sock.bind((ACTIVE_IP, RECV_UDP_PORT))                                           #Bind Socket
    raw_message, client = sock.recvfrom(DATAGRAM_SIZE)                              #Recieve Data
    if raw_message[0:2] == MAGIC_BYTES:                                             #Check if data is from a client of ours using the "Magic Bytes"
        try:
            Incoming_Message_Queue.puts(json.loads(raw_message[2:0].decode()))      #Attempt to deserialize the json message into a python dict and put it in the queue.
        except:
            return
    else:
        return
    
