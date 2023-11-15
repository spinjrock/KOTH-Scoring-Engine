#A very basic idea for the scoring agent

#Imports
import asyncio
import socket
import json
import logging

#Constant Declarations
LOOPBACK_IP = "127.0.0.1"
RECV_UDP_PORT = 50435
DATAGRAM_SIZE = 2048
MAGIC_BYTES = b"\x13\x90"
CONFIG_PATH = "config.json"

#Globals
Scoring_Engine_Ip = ""
Flag_Path = ""
Machine_Name = ""
Active_Ip = Scoring_Engine_Ip

async def check_flag():
    try:
        logging.info(f"Checking Flag: {Flag_Path}")
        with open(Flag_Path, "r") as flag_file:
            flag_content = flag_file.read().strip()
            return flag_content
    except:
        return

async def send_message():
    logging.info("Starting Send Message Function")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    flag_content = await check_flag()
    data = {
        "flag_content": flag_content,
        "machine_name": Machine_Name

    }
    json_message = json.dumps(data).encode()
    message = MAGIC_BYTES + json_message
    logging.info(f"Sending: {str(message)}")
    sock.sendto(message, (ACTIVE_IP, RECV_UDP_PORT))

async def main():
    logging.info("Starting Async Main Function")
    while True:
        await asyncio.gather(send_message())
        await asyncio.sleep(60)

if __name__ == "__main__":
    logging.basicConfig(format = "",level=logging.INFO)
    logging.info("Started As Main")
    logging.info(f"Reading Config: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r") as conf:
        config = json.load(conf)
        Scoring_Engine_Ip = config["Scoring_Engine_Ip"]
        Machine_Name = config["Machine_Name"]
        Flag_Path = config["Flag_Path"]
        Active_Ip = Scoring_Engine_Ip
    logging.info("Read Config:")
    logging.info(f"Machine_Name: {Machine_Name}")
    logging.info(f"Flag_Path: {Flag_Path}")
    logging.info(f"Scoring_Engine_Ip: {Scoring_Engine_Ip}")
    asyncio.run(main())