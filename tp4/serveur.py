from hashlib import sha256
from socketUtil import recv_msg, send_msg
import getpass
import socket
import os.path
import sys
import re
import smtplib
from email.mime.text import MIMEText
import email.generator


def main():
    try:
        port = 6969
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(("localhost", port))
        serversocket.listen(5)
        print("Serveur en ecoute sur le port {0}".format(str(port)))
        (s, address) = serversocket.accept()
        number = ""
        while (number != "1" and number != "2"):
            number = recv_msg(s)
        success = False
        while (not success):
            username = recv_msg(s)
            password = recv_msg(s)
            configPath = os.path.join(getServerPath(),username, "config.txt")
            if number == "1":
                if(os.path.exists(configPath)):
                    hashedPass = sha256(password.encode()).hexdigest()
                    with open(configPath, "r") as configFile:
                            configPassword = configFile.readline()
                            if configPassword == hashedPass:
                                send_msg(s, "Connection reussie")
                                success = True
                                courriel(s, username)
                            else:
                                send_msg(s, "Nom d'utilisateur et mot de passe invalides")
                else:
                    send_msg(s, "L'utilisateur n'existe pas!")
            elif number == "2":
                if(os.path.exists(configPath)):
                    send_msg(s, "L'utilisateur existe deja!")
                else:
                    if(re.search(r"(?=[^a-zA-Z]*[a-zA-Z])(?=[^\d]*\d+)(^.{6,12}$)", password) and re.search(r"^[^@]+@[^@]+\.[^@]+$", username):
                        hashedPass = sha256(password.encode()).hexdigest()
                        os.makedirs(os.path.join(getServerPath(),username), exist_ok=True)
                        with open(configPath, "w") as configFile:
                            configFile.write(hashedPass)
                            send_msg(s, "Creation de l'utilisateur terminee")
                            success = True
                            courriel(s, username)
                    else:
                        send_msg(s, "Erreur: le mot de passe doit etre compose de 6 a 12 \
                            caracteres, dont au moins un chiffre et une lettre et le nom d'utilisateur \
                            doit etre une adresse courriel")
    except socket.error as msg:
        print ("Socket Error: %s" % msg)
    except TypeError as msg:
        print ("(Le client s'est probablement deconnecte) Type Error: %s" % msg)


def courriel(s, username):
    while True:
        number = ""
        while (number != "1" and number != "2" and number != "3"and number != "4"):
            number = recv_msg(s)
        if (number == "1"):
            emailDestination = ""
            while (not re.search(r"^[^@]+@[^@]+\.[^@]+$", emailDestination)):
                emailDestination = recv_msg(s)
            subject = recv_msg(s)
            message = recv_msg(s)
            msgToSend = MIMEText(message)
            msgToSend["From"] = username
            msgToSend["To"] = emailDestination
            msgToSend["Subject"] = subject
            if(re.search(r"^[^.@]+(@reseauglo.ca)$", emailDestination)):
                cheminDossierDestination = os.path.join(getServerPath(),emailDestination)
                if os.path.exists(cheminDossierDestination):
                    with open(os.path.join(cheminDossierDestination,subject + '.elm'), 'w') as out:
                        gen = email.generator.Generator(out)
                        gen.flatten(msgToSend)
                    send_msg(s,"Succes de depot du courriel dans le dossier utilisateur")
                else:
                    send_msg(s,"Erreur : l'utilisateur n'existe pas")
            else:
                try:
                    smtpConnection = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
                    smtpConnection.sendmail(msgToSend["From"], msgToSend["To"], msgToSend.as_string())
                    smtpConnection.quit()
                    msg = "Le courriel a bien ete envoye!"
                except:
                    msg = "L’envoi n’a pas pu etre effectue."
                send_msg(s,msg)
        elif (number == "2"):
            # TODO:
        elif (number == "3"):
            # TODO:
        elif (number == "4"):
            quit()




def getServerPath():
    return os.path.dirname(os.path.realpath(__file__))

while 1:
    if __name__ == '__main__':
        main()
