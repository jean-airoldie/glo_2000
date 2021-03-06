from hashlib import sha256
from socketUtil69 import recv_msg, send_msg, SocketDisconnect
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
                    if(re.search(r"(?=[^a-zA-Z]*[a-zA-Z])(?=[^\d]*\d+)(^.{6,12}$)", password) and re.search(r"^[^@]+@[^@]+\.[^@]+$", username)):
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
    except SocketDisconnect as e:
        print ("Client deconnecté : {}".format(e))


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
                userPathDestination = os.path.join(getServerPath(),emailDestination)
                if os.path.exists(userPathDestination):
                    with open(os.path.join(userPathDestination,subject + '.elm'), 'w') as out:
                        gen = email.generator.Generator(out)
                        gen.flatten(msgToSend)
                    send_msg(s,"Le courriel a bien ete envoye!")
                else:
                    os.makedirs(os.path.join(getServerPath(), "DESTERREUR"), exist_ok = True)
                    send_msg(s,"Erreur : l'utilisateur n'existe pas")
                    with open(os.path.join(getServerPath(),"DESTERREUR", subject + '.elm'), 'w') as out:
                        gen = email.generator.Generator(out)
                        gen.flatten(msgToSend)
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
            userPath = os.path.join(getServerPath(),username)
            subjectsList = []
            for fileName in os.listdir(userPath):
                if fileName.split(".")[-1] == "elm":
                    subject = ".".join(fileName.split(".")[:-1])
                    subjectsList.append(subject)
            strBuffer = "\n"
            if subjectsList:
                for i, subject in enumerate(subjectsList):
                     strBuffer += "{} : {}\n".format(i+1, subject)
                send_msg(s, strBuffer)
            else:
                send_msg(s, "no_messages")
            valid = False
            while not valid:
                subjectNumber = recv_msg(s)
                assert subjectNumber
                if int(subjectNumber) > 0 and int(subjectNumber) < len(subjectsList) + 1:
                    valid = True
                    send_msg(s, "valid_response")
                    strBuffer = ""
                    with open(os.path.join(getServerPath(), username, "{}.elm".
                                           format(subjectsList[int(subjectNumber) - 1])), "r") as f:
                        strBuffer = "\n"
                        for i, line in enumerate(f):
                            if i > 3:
                                strBuffer += line
                        strBuffer += "\n"
                    send_msg(s, strBuffer)
                else:
                    send_msg(s, "invalid_response")
                    break

        elif (number == "3"):
            userPath = os.path.join(getServerPath(), username)
            count = 0
            octets = 0
            subjectsList = []
            for fileName in os.listdir(userPath):
                octets += os.path.getsize(os.path.join(userPath, fileName))
                if fileName.split(".")[-1] == "elm":
                    count += 1
                    subject = ".".join(fileName.split(".")[:-1])
                    subjectsList.append(subject)
            strBuffer = "{} messages dans le dossier de {}\n".format(count, username)
            strBuffer += "Taille total du dossier {} octets\n".format(octets)
            if len(subjectsList) > 0:
                for i, subject in enumerate(subjectsList):
                    strBuffer += "{} : {}\n".format(i+1, subject)
            else:
                strBuffer += "Aucun messages dans le dossier de {}".format(username)
            send_msg(s, strBuffer)

        elif (number == "4"):
            break

def getServerPath():
    return os.path.dirname(os.path.realpath(__file__))

while 1:
    if __name__ == '__main__':
        main()
