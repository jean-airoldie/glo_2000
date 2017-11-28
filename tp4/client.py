from socketUtil import recv_msg, send_msg
import getpass
import socket


def main():
    s = connection()
    try:
        number = ""
        while(number != "1" and number != "2"):
            number = input("Menu de connexion \n1.Se connecter\n2.Creer un compte\n")
            if number != "1" and number != "2":
                print("Veuillez choisir l'option 1 ou 2...")
        username = input("Entrez votre nom d'usager: ")
        password = getpass.getpass("Mot de passe : ")
        send_msg(s, number)
        send_msg(s, username)
        send_msg(s, password)
        serverConfirmation = ""
        while(serverConfirmation != "Creation de l'utilisateur terminee"):
            serverConfirmation = recv_msg(s)
            print(serverConfirmation)
            if serverConfirmation != "Creation de l'utilisateur terminee":
                username = input("Entrez votre nom d'usager: ")
                password = getpass.getpass("Mot de passe : ")
                send_msg(s, username)
                send_msg(s, password)
    except socket.error as e:
        print("Erreur de socket: %s. Tentative de reconnection" % e)


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


while 1:
    if __name__ == '__main__':
        main()
