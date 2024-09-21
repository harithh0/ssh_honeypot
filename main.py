import logging
import os
import socket
import threading
from random import uniform
from time import sleep

import paramiko
import requests
from dotenv import load_dotenv

logging.getLogger("paramiko").setLevel(logging.CRITICAL)
logging.basicConfig(
    filename="ssh_server.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",  # timestamp
)
logger = logging.getLogger(__name__)


def createRSAKey():
    key = paramiko.RSAKey.generate(2048)
    key.write_private_key_file("key")


# optional get geo location (required IPINFO API KEY)
def get_location(ip):
    format = ""
    try:
        load_dotenv()
        token = os.getenv("GEO_API_KEY")
        response = requests.get(f"https://ipinfo.io/{ip}?token{token}")
        if response.status_code == 200:
            data = response.json()
            if data.get("bogon"):
                format += "bogus ip (maybe lan IP?)"
                return format
            format += f"{data.get('city')}, {data.get('region')}, {data.get('country')}"
    except Exception as e:
        print("error:", e)
    return format


class SSHServer(paramiko.ServerInterface):

    def __init__(self, user_ip, geolocation):
        self.user_ip = user_ip
        self.geolocation = geolocation

    def check_auth_password(self, username: str, password: str) -> int:
        logger.info(f"{self.user_ip} @ {self.geolocation} - '{username}':'{password}'")
        sleep(uniform(0, 3))
        return paramiko.AUTH_FAILED


def handle_connection(client_sock, client_addr):
    transport = paramiko.Transport(
        client_sock
    )  # take this socket and use it to run as  an ssh server
    transport.local_version = "SSH-2.0-OpenSSH_5.1"
    if not os.path.exists("key"):
        createRSAKey()

    server_key = paramiko.RSAKey.from_private_key_file("key")
    transport.add_server_key(server_key)
    user_ip = client_addr[0]
    geolocation = get_location(str(user_ip))
    ssh = SSHServer(user_ip, geolocation)
    transport.start_server(server=ssh)


def main():

    IP = ""
    PORT = 22
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((IP, PORT))
    while True:
        server_sock.listen(223)
        client_sock, client_addr = server_sock.accept()
        print(f"connection from: {client_addr[0]}:{client_addr[1]}")
        t = threading.Thread(
            target=handle_connection, args=((client_sock, client_addr))
        )

        t.start()


if __name__ == "__main__":
    main()
