from socketUtil import recv_msg, send_msg
import getpass
import socket


def main():
    number = input("Menu de connexion \n1. Se connecter\n2.Creer un compte\n")
    if number != "1" and number != "2":
        print("Veuillez choisir l'option 1 ou 2...")
    else:
        username = input("Entrez votre nom d'usager: ")
        password = getpass.getpass('Mot de passe : ')
        destination = ("localhost", 69420)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(destination)
        send_msg(s, number)
        send_msg(s, username)
        send_msg(s, password)
        s.close()
