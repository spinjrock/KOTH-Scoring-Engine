#A very basic idea for the scoring engine

#Imports
import asyncio
import queue
import socket
import json
import threading
import time
import logging

#Constant Declarations
HOST_IP = socket.gethostbyname(socket.gethostname())
LOOPBACK_IP = "127.0.0.1"
RECV_UDP_PORT = 50435
DATAGRAM_SIZE = 2048
ACTIVE_IP = LOOPBACK_IP
MAGIC_BYTES = b"\x13\x90"
TICK = 60

class Machine:
    last_heard_from = 0
    name = ""
    current_flag = ""

class Team:
    points = 0
    flag = ""

#Globals
Incoming_Message_Queue = queue.Queue()
Teams = []
Machines = []

async def recv_message():
    logging.info(f"Recieveing Messages on {ACTIVE_IP}:{RECV_UDP_PORT}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                         #Initialize Socket
    sock.bind((ACTIVE_IP, RECV_UDP_PORT))                                           #Bind Socket
    raw_message, client = sock.recvfrom(DATAGRAM_SIZE)                              #Recieve Data
    logging.info(f"Message Recieved from {str(client)}")
    if raw_message[0:2] == MAGIC_BYTES:                                             #Check if data is from a client of ours using the "Magic Bytes"
        try:
            Incoming_Message_Queue.puts(json.loads(raw_message[2:0].decode()))      #Attempt to deserialize the json message into a python dict and put it in the queue.
        except:
            return
    else:
        return

async def update_machines():
    logging.info("Updating Machines")
    while Incoming_Message_Queue.qsize() > 0:
        message = Incoming_Message_Queue.get()
        for machine in Machines:
            if machine.name == message.machine_name:
                machine.last_heard_from = f"{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime.tm_sec}"
                machine.current_flag = message.flag_content

async def main():
    logging.info("Starting Server Main Function")
    while True:
        await asyncio.gather(update_machines(), recv_message())

def thread_tick():
    logging.info("Starting tick thread")
    while True:
        for machine in Machines:
            for team in Teams:
                if team.flag == machine.current_flag:
                    team.points = team.points+1
        logging.info(f"tick: {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}")
        time.sleep(60)

def thread_server():
    logging.info("Starting server thread")
    asyncio.run(main())

if __name__ == "__main__":
    logging.basicConfig(format = "",level=logging.INFO)
    tick = threading.Thread(target=thread_tick)
    server = threading.Thread(target=thread_server)
    tick.start()
    server.start()
    server.join()
    tick.join()