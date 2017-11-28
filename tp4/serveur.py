from hashlib import sha256
from socketUtil import recv_msg, send_msg
import getpass
import socket


def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(("localhost", 69420))
    serversocket.listen(5)
    (s, address) = serversocket.accept()
    number = recv_msg(s)
    username = recv_msg(s)
    hashedPass = recv_msg(s)
