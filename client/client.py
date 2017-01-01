#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
import socket
from lib.msgSender import *
import time



hote = "localhost"
port = 12800

########################################################################################################################
#                                                                                                                      #
#                                       Initialisation du client                                                       #
#                                                                                                                      #
########################################################################################################################
connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connexion_avec_serveur.connect((hote, port))
msg_recu = connexion_avec_serveur.recv(1024)

if msg_recu.decode() == "closed":
    print("Les inscriptions sont closes sur le serveur")

elif msg_recu.decode() == "ok":
    print("Connexion établie avec le serveur sur le port {}".format(port))

    """enregistrement du nom du joueur si le nom est déjà pris, on repose la question"""
    while True:
        name = input("Quel est votre nom ? > ")
        connexion_avec_serveur.send(name.encode())

        msg_recu = connexion_avec_serveur.recv(1024)
        if msg_recu.decode() == "already_exist":
            print("Ce pseudo est déjà pris, merci d'en choisir un autre")
        else:
            print("Bienvenue dans le jeu {}".format(name))
            print(msg_recu.decode())
            break

    """enregistrement du symbole du joueur si le symbole est déjà pris, on repose la question"""
    while True:
        symbol = input("Quelle sera la lettre qui vous représentera ? > ")
        connexion_avec_serveur.send(symbol.encode())

        msg_recu = connexion_avec_serveur.recv(1024)
        if msg_recu.decode() == "already_exist":
            print("Ce symbole est déjà pris, merci d'en choisir un autre")
        elif msg_recu.decode() == "to_long":
            print("Trop long, vous ne pouvez choisir qu'un seul caractère")
        elif msg_recu.decode() == "reserved":
            print("Caractère réservé, vous ne pouvez pas prendre le U, le O, le . et le |")
        else:
            print(msg_recu.decode())
            break
# -------------------------------------------------------------------------------------------------------------------- #

########################################################################################################################
#                                                                                                                      #
#              Mise en place de 3 Threads pour gestion du statut // aux ordres  // messages reçus                      #
#                                                                                                                      #
########################################################################################################################
    thread_1 = MsgSender(connexion_avec_serveur)
    thread_2 = StatusSender(connexion_avec_serveur)
    thread_3 = MsgRecever(connexion_avec_serveur)

    thread_1.start()
    thread_2.start()
    thread_3.start()

    thread_1.join()
    thread_2.join()
    thread_3.join()

# -------------------------------------------------------------------------------------------------------------------- #

    print("Fermeture de la connexion")

    connexion_avec_serveur.close()
