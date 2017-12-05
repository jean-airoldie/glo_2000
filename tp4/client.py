from socketUtil import recv_msg, send_msg
import getpass
import socket
import re
import os.path
def main():
    s = connection()
    try:
        number = ""
        while(number != "1" and number != "2"):
            number = input("Menu de connexion \n1. Se connecter\n2. Creer un compte\n")
            if number != "1" and number != "2":
                print("Veuillez choisir l'option 1 ou 2...\n")
        username = input("Entrez votre nom d'usager: ")
        password = getpass.getpass("Mot de passe : ")
        send_msg(s, number)
        send_msg(s, username)
        send_msg(s, password)
        serverConfirmation = ""
        while(not (serverConfirmation == "Creation de l'utilisateur terminee" or serverConfirmation == "Connection reussie")):
            serverConfirmation = recv_msg(s)
            print(serverConfirmation + "\n")
            if not (serverConfirmation == "Creation de l'utilisateur terminee" or serverConfirmation == "Connection reussie"):
                username = input("Entrez votre nom d'usager: ")
                password = getpass.getpass("Mot de passe : ")
                send_msg(s, username)
                send_msg(s, password)
        menu(s)
    except socket.error as e:
        print("Erreur de socket: %s. Tentative de reconnection\n" % e)


def connection():
    connected = False
    while (not connected):
        try:
            destination = ("localhost", 6969)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(destination)
            connected = True
        except Exception as e:
            retry = input("Erreur de connection au serveur : %s. Reessayer la connection? (O ou N)\n" % e)
            if str.upper(retry) == "O":
                pass
            elif str.upper(retry) == "N":
                quit()
    return s


def menu(s):
    number = ""
    while (number != "1" and number != "2" and number != "3"and number != "4"):
        number = input("Menu principal\n1. Envoi de courriels\n2. Consultation de courriels\n3. Statistiques\n4. Quitter\n")
        if(number != "1" and number != "2" and number != "3"and number != "4"):
            print("Veuillez choisir une option valide")
        else:
            send_msg(s,number)
            if(number == "1"):
                serverConfirmation = ""
                while(not serverConfirmation == "Le courriel a bien ete envoye!"):
                    emailDestination = ""
                    while (not re.search(r"^[^@]+@[^@]+\.[^@]+$", emailDestination)):
                        emailDestination = input("Entrez une adresse courriel de destination\n")
                        if(re.search(r"^[^@]+@[^@]+\.[^@]+$", emailDestination)):
                            subject = input("Entrez le sujet du courriel\n")
                            message = input("Entrez le corps du message\n")
                            send_msg(s, emailDestination)
                            send_msg(s, subject)
                            send_msg(s, message)
                            serverConfirmation = recv_msg(s)
                            print(serverConfirmation)
                        else:
                            print("Adresse courriel invalide\n")


while 1:
    if __name__ == '__main__':
        main()
