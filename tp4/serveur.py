from hashlib import sha256
from socketUtil import recv_msg, send_msg
import getpass
import socket
import os.path
import re


def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(("localhost", 69420))
    serversocket.listen(5)
    (s, address) = serversocket.accept()
    number = recv_msg(s)
    username = recv_msg(s)
    password = recv_msg(s)
    if number == "1":
        print("Topkekekeke\n")
    elif number == "2":
        configPath = str.format(username, "/{0}/config.txt")
        if(os.path.exists(configPath)):
            send_msg(s, "L'utilisateur existe déjà!")
        else:
            if(re.search(r"(?=[^a-zA-Z]*[a-zA-Z])(?=[^\d]*\d+)(^.{6,12}$)", password)):
                hashedPass = sha256(password.encode()).hexdigest()
                os.makedirs(os.path.dirname(configPath), exist_ok=True)
                with open(configPath, "w") as configFile:
                    f.write(hashedPass)
                    send_msg(s, "Création de l'utilisateur terminée")
            else:
                send_msg(s, "Erreur: le mot de passe doit être composé de 6 à 12 caractères, dont au moins un chiffre et une lettre")
