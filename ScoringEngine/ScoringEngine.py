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
CONFIG_PATH = "config.json"

class Machine:
    last_heard_from = 0
    name = ""
    current_flag = ""
    def __init__(self, machine_name: str):
        self.name = machine_name
    def to_dict(self):
        d = {}
        d["name"] = self.name
        d["current_flag"] = self.current_flag
        d["last_heard_from"] = self.last_heard_from
        return d

class Team:
    points = 0
    flag = ""
    def __init__(self, team_name: str):
        self.flag = team_name
    def to_dict(self):
        d = {}
        d["points"] = self.points
        d["flag"] = self.flag
        return d

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
        logging.info(f"    Message:{raw_message[2:]}")
        try:
            Incoming_Message_Queue.put(json.loads(raw_message[2:].decode()))      #Attempt to deserialize the json message into a python dict and put it in the queue.
        except Exception as err:
            logging.info(f"    {err}")
            return
    else:
        return

async def update_machines():
    logging.info("Updating Machines")
    while Incoming_Message_Queue.qsize() > 0:
        message = Incoming_Message_Queue.get()
        logging.info(f"    Message:{message}")
        for machine in Machines:
            if machine.name == message["machine_name"]:
                logging.info(f"    Updating Machine: {machine.name}")
                machine.last_heard_from = f"{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
                machine.current_flag = message["flag_content"]

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
        logging.info(f"{[team.flag for team in Teams]}")
        logging.info(f"{[team.points for team in Teams]}")
        for machine in Machines:
            d= {}
            d[machine.name] = machine.to_dict()
            with open("machines.json", "w") as m:
                json.dump(d, m)
        for team in Teams:
            d = {}
            d[team.flag] = team.to_dict()
            with open("teams.json", "w") as t:
                json.dump(d, t)
        time.sleep(60)

def thread_server():
    logging.info("Starting server thread")
    asyncio.run(main())

if __name__ == "__main__":
    logging.basicConfig(format = "",level=logging.INFO)
    logging.info(f"Reading config file: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r") as conf:
        config = json.load(conf)
        for team_name in config["teams"]:
            aTeam = Team(team_name)
            Teams.append(aTeam)
        for machine_name in config["machines"]:
            aMachine = Machine(machine_name)
            Machines.append(aMachine)
    logging.info(f"Teams: {[team.flag for team in Teams]}")
    logging.info(f"Machines: {[machine.name for machine in Machines]}")
    tick = threading.Thread(target=thread_tick)
    server = threading.Thread(target=thread_server)
    tick.start()
    server.start()
    server.join()
    tick.join()