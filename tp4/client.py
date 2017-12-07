from socketUtil69 import recv_msg, send_msg, SocketDisconnect
import getpass, sys, socket, re, os.path, signal


class Client:
    def __init__(self):
        self.is_connected = False
        signal.signal(signal.SIGINT, self.on_keyboard_interrupt)
        self.connect()

    def connect(self):
            try:
                destination = ("localhost", 6969)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(destination)
                self.s = s
                is_connected = True
            except Exception as e:
                retry = input("Erreur de connection au serveur : "
                        "%s. Reessayer la connection? (O ou N)\n" % e)
                if retry.upper() == "O":
                    self.connect()
                elif retry.upper() == "N":
                    self.close()

    def close(self):
        send_msg(self.s, "4")
        if self.is_connected:
            self.s.shutdown(2)
            self.s.close()
        sys.exit(0)

    def on_keyboard_interrupt(self, signal, frame):
        self.close()

    def main(self):
        s = self.s
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
            self.menu()
        except socket.error as e:
            print("Erreur de socket: %s. Tentative de reconnection\n" % e)
        except SocketDisconnect as e:
            print("Deconnection du socket : {}".format(e))

    def menu(self):
        s = self.s
        while True:
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
                    elif(number == "2"):
                        subjectsList = recv_msg(s)
                        if subjectsList == "no_messages":
                            print("Aucun messages à afficher")
                            print()
                        else:
                            print(subjectsList)
                            valid = False
                            while not valid:
                                subjectNumber = input("Numero de sujet a consulter:")
                                try:
                                    int(subjectNumber)
                                    assert subjectNumber
                                    send_msg(self.s, str(subjectNumber))
                                    response = recv_msg(self.s)
                                    valid = True if response == "valid_response" else False
                                    if not valid:
                                        print("Numero de message invalide")
                                except ValueError:
                                    print("Le numero de message doit etre de type 'int'")
                            selectedSubject = recv_msg(s)
                            print(selectedSubject)
                    elif(number == "3"):
                        response = recv_msg(s)
                        print(response)
                        input()

                    elif(number == "4"):
                        sys.exit(0)


if __name__ == '__main__':
    client = Client()
    client.main()
