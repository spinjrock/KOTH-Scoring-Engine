#A very basic idea for the scoring agent

#Imports
import asyncio
import socket
import json

#Constant Declarations
SCORING_ENGINE_IP = ""  #Read from config file?
FLAG_PATH = ""
MACHINE_NAME = ""
LOOPBACK_IP = "127.0.0.1"
RECV_UDP_PORT = 50435
DATAGRAM_SIZE = 2048
ACTIVE_IP = LOOPBACK_IP
MAGIC_BYTES = b"\x13\x90"

#Globals


async def check_flag():
    try:
        with open(FLAG_PATH, "r") as flag_file:
            flag_content = flag_file.get_content.strip()
            return flag_content
    except:
        return

async def send_message():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    flag_content = await check_flag()
    data = {
        "flag_content": flag_content,
        "machine_name": MACHINE_NAME

    }
    json_message = json.dumps(data).encode()
    message = MAGIC_BYTES + json_message
    print(message)
    sock.sendto(message, (ACTIVE_IP, RECV_UDP_PORT))

async def main():
    while True:
        await asyncio.gather(send_message())
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())