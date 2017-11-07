import socket, optparse, sys
from socketUtil import recv_msg, send_msg
from cryptoModule import (
        entierAleatoire, estProbablementPremier, trouverNombrePremier, 
        exponentiationModulaire
        )
import logging, datetime as dt

# Choisissez l’adresse avec l’option -a et le port avec -p
parser = optparse.OptionParser()
parser.add_option("-s", "--serveur", action="store_true", dest="serveur", default=False)
parser.add_option("-d", "--destination", action="store", dest="destination", default=None)
parser.add_option("-p", "--port", action="store", dest="port", type=int, default=None)
opts = parser.parse_args(sys.argv[1:])[0]

logging.basicConfig(level=logging.DEBUG, filename="Error.log")

def main():
    if type(opts.port) is not int:
        raise ValueError("The --port value must be assigned")
    if opts.serveur == True and opts.destination is not None:
        raise ValueError("Args --destination and --server are mutually exclusive")
    if opts.serveur: 
        # En mode serveur
        """ Setup socket """
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind(("localhost", opts.port))
        serversocket.listen(5)
        (s, address) = serversocket.accept()
        """ Genere modulo, base """
        modulo = trouverNombrePremier()
        base = entierAleatoire(modulo)
        """ Send modulo and base to client """
        send_msg(s, str(modulo))
        send_msg(s, str(base))
        """ Genere cle privee """
        cle_privee = entierAleatoire(modulo)
        """ Genere cle publique """
        cle_publique = exponentiationModulaire(base, cle_privee, modulo)
        """ Envoit sa cle publique """
        send_msg(s, str(cle_publique))
        """ Recoit cle publique client """
        client_cle_publique = int(recv_msg(s))
        """ Genere cle partagee"""
        cle_partagee = exponentiationModulaire(client_cle_publique, cle_privee, modulo)
        print(cle_partagee)
        s.close()
    else: 
        # En mode client
        destination = (opts.destination, opts.port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(destination)
        """ Genere modulo, base """
        modulo = int(recv_msg(s))
        base = int(recv_msg(s))
        """ Genere sa cle privee """
        cle_privee = entierAleatoire(modulo)
        """ Genere sa cle publique """
        cle_publique = exponentiationModulaire(base, cle_privee, modulo)
        """ Recoit cle publique serveur """
        serveur_cle_publique = int(recv_msg(s))
        """ Envoit sa cle publique """
        send_msg(s, str(cle_publique))
        """ Genere cle partagee"""
        cle_partagee = exponentiationModulaire(serveur_cle_publique, cle_privee, modulo)
        print(cle_partagee)
        s.close()

if __name__ == "__main__":
    try:
        main()
    except ValueError:
        logging.exception("at datetime {} :\n".format(dt.datetime.now()))
        raise
