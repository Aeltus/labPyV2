#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import os
import socket
import select
import time
from lib.files import Files
from lib.player import Player
from lib.compartment import Compartment
from lib.mapManager import *
from lib.GameManager import *

"""Controlleur frontal du serveur"""

hote = ''
port = 12800

########################################################################################################################
#                                                                                                                      #
#                                       Initialisation de la map                                                       #
#                                                                                                                      #
########################################################################################################################
data = {}
print("Bienvenue sur Roboc, le jeu de labyrinthe en réseau développé pour OC \n")

maps = os.listdir("dic/maps/")
i = 0
print("Quelle carte choisissez vous ?\n")
for (i, map_name) in enumerate(maps):
    print("{0}- {1}".format(i + 1, map_name[0:-4]))

while True:
    numMap = input("Entrez le numero du labyrinthe pour commencer à jouer : ")
    try:
        int(numMap)
        if 0 < int(numMap) < i + 1:
            numMap = int(numMap) - 1
            break
        else:
            print("Merci d'entrer un numero de carte valide")
    except ValueError:
        print("Merci d'entrer le NUMERO de la carte")

print("Carte : {0}".format(maps[numMap][0:-4]))

content = Files.fopen("dic/maps/" + maps[numMap])

initialised = MapManager.map_initialiser(content)
data = initialised[0]  # la map sous forme de dictionnaire d'objets
max_x = initialised[1]  # nombre max de colonnes dans la map initialisée
max_y = initialised[2]  # nombre max de lignes dans la map initialisée

# -------------------------------------------------------------------------------------------------------------------- #

########################################################################################################################
#                                                                                                                      #
#                                       Initialisation du serveur                                                      #
#                                                                                                                      #
########################################################################################################################

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)

print("Le serveur écoute à présent sur le port {}".format(port))

serveur_lance = True
session_start = False
game_started = False
clients_connectes = []
tour = 0
joueurs = {}
winner = ""

while serveur_lance:

    msg_envoi = ""
    requette = ""
    # On va vérifier que de nouveaux clients ne demandent pas à se connecter
    # Pour cela, on écoute la connexion_principale en lecture
    # On attend maximum 50ms

    connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)

    for connexion in connexions_demandees:

        connexion_avec_client, infos_connexion = connexion.accept()

        """Si la session n'est pas démarrée on enregistre la connection"""
        if session_start is False:
            # On ajoute le socket connecté à la liste des clients
            connexion_avec_client.send(b"ok") # renvoie le message ok au client pour signifier que l'enregistrmeent c'est bien passé
            clients_connectes.append(connexion_avec_client)
            joueurs[connexion_avec_client] = Player()

            """Si la session de jeu est démarrée on rejette la connection"""
        else:
            connexion_avec_client.send(b"closed") # renvoie le message closed au client qui en deduit que la connection est fermée
            connexion_avec_client.close()

    # Maintenant, on écoute la liste des clients connectés
    # Les clients renvoyés par select sont ceux devant être lus (recv)
    # On attend là encore 50ms maximum
    # On enferme l'appel à select.select dans un bloc try
    # En effet, si la liste de clients connectés est vide, une exception
    # Peut être levée

    clients_a_lire = []

    try:
            clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05)

    except select.error:
        pass

    else:
        # On parcourt la liste des clients à lire
        for client in clients_a_lire:

            # Client est de type socket
            msg_recu = client.recv(1024)

            # Peut planter si le message contient des caractères spéciaux
            msg_recu = msg_recu.decode()

# -------------------------------------------------------------------------------------------------------------------- #

########################################################################################################################
#                                                                                                                      #
#                                                 Le jeu                                                               #
#                                                                                                                      #
########################################################################################################################
            """

            Les messages reçus par le serveur sont stoqués l'un à la suite de l'autre tant qu'ils n'ont pas été lu par le
            serveur. Pour m'assurer de traiter les envois l'un après l'autre, j'encadre mes envois par le symbole | .
            Ainsi, une fois reçu j'obtiens soit un seul message de type |message| ou |message1||message2|.
            Il suffit de parser le message reçu, et de le traiter par paquet pour traiter message1, puis message2.

            """

            paquet = msg_recu.split("|")
            a = 0
            while a < len(paquet):
                """ Actions pour chaque ordre reçu dans le paquet en cours"""
                if paquet[a] != "":

                    """Dès qu'un client demande le statut du jeu, on le lui envoie"""
                    if game_started is True:
                        """Traitement des requettes de statut"""
                        if paquet[a] == "status":
                            """on détermine à qui le tour de jouer"""

                            joueur_en_cour = ""
                            for joueur in joueurs.values():
                                if joueur.tour == 1:
                                    joueur_en_cour = joueur.name
                                    break

                            """ A chaque demande de statut, on envoie le joueur qui doit jouer et la map sous forme de srting"""
                            msg_envoi = "Au tour de : {}|{}\n".format(joueur_en_cour,  MapManager.get_string_map_from_dic(data))

                            if joueurs[client].tour == 1 and joueurs[client].requette != "":
                                requette = joueurs[client].requette
                                action = requette[0]
                                direction = requette[1]
                                vitesse = int(requette[2])

                                vitesse -= 1

                                if vitesse > 0:
                                    joueurs[client].requette = (action, direction, vitesse)
                                else:
                                    joueurs[client].requette = ""

                                new_loc_y = joueurs[client].y
                                new_loc_x = joueurs[client].x

                                if direction == "n":
                                    new_loc_y -= 1
                                elif direction == "s":
                                    new_loc_y += 1
                                elif direction == "e":
                                    new_loc_x += 1
                                elif direction == "o":
                                    new_loc_x -= 1

                                new_loc = (new_loc_x, new_loc_y)

                                if action == "m":
                                    if data[new_loc].content == ".":
                                        data[new_loc].content = "O"
                                        if data[new_loc].visible == ".":
                                            data[new_loc].visible = "O"
                                        joueurs = GameManager.joueur_suivant(joueurs)
                                    else:
                                        msg_envoi = "|Ce n'est pas une porte\n Une autre idee ?|"
                                        joueurs[client].requette = ""

                                elif action == "p":
                                    if data[new_loc].content == "O":
                                        data[new_loc].content = "."
                                        if data[new_loc].visible == "O":
                                            data[new_loc].visible = "."
                                        joueurs = GameManager.joueur_suivant(joueurs)
                                    else:
                                        msg_envoi = "|Ce n'est pas un mur\n Une autre idee ?|"
                                        joueurs[client].requette = ""

                                elif action == "a":
                                    if data[new_loc].content in [" ", "."]:
                                        player_loc = (joueurs[client].x, joueurs[client].y)
                                        data[player_loc].visible = data[player_loc].content
                                        data[new_loc].visible = joueurs[client].symbol
                                        joueurs[client].x = new_loc_x
                                        joueurs[client].y = new_loc_y
                                        joueurs = GameManager.joueur_suivant(joueurs)

                                    elif data[new_loc].content == "U":
                                        winner = joueurs[client].name
                                    else:
                                        msg_envoi = "|Vous vous heurtez a un mur\n Une autre proposition ?|"
                                        joueurs[client].requette = ""

                                else:
                                    msg_envoi = "|action non reconue|"
                                    joueurs[client].requette = ""


                            """ Pour les commandes, on écoute que le joueur à qui c'est le tour, les autres sont jettées """
                        elif joueurs[client].tour == 1 and paquet[a][0] in ["n", "s", "e", "o", "m", "p"]:
                            if joueurs[client].requette == "":
                                joueurs[client].requette = GameManager.request_analyser(paquet[a])

# -------------------------------------------------------------------------------------------------------------------- #

########################################################################################################################
#                                                                                                                      #
#                                   Séquence initialisation et contrôles                                               #
#                                                                                                                      #
########################################################################################################################

                    """ fin => fermeture du programme """
                    if paquet[a] == "fin":  # message indiquant le fin de l'execution => renvoie fin aux threads et stoppe le serveur
                        msg_envoi = "|Fin de la partie|fin|appuyez sur entree pour sortir|"
                        for client in clients_connectes:
                            client.send(msg_envoi.encode())
                        serveur_lance = False
                        time.sleep(1)

                    """ Quelque soit l'ordre reçu si la session est lancée, mais le jeu non démarré, on initialise le jeu """
                    if session_start is True and game_started is False:
                        initilised = GameManager.game_init(joueurs, data, max_x, max_y)
                        joueurs = initilised[0]
                        data = initilised[1]
                        print(MapManager.get_string_map_from_dic(data))
                        print(len(joueurs))
                        game_started = True
                        joueurs[client].step = "running"

                    """ Si la session n'est pas démarrée mais le symbole du joueur est défini """
                    if joueurs[client].step == "sessionInit":
                        session = GameManager.session_init(paquet[a], joueurs, client)
                        session_start = session[1]
                        msg_envoi = session[0]
                        joueurs = session[2]

                    """Paramétrage du symbole lors de la connection"""
                    if joueurs[client].step == "defSymbol":
                        # si plus d'un caractère
                        if len(msg_recu) > 1:
                            msg_envoi = "to_long"
                            # si c'est un caractère utilisé dans le jeu
                        elif msg_recu in ["U", "u", "O", "o", ".", "|"]:
                            msg_envoi = "reserved"
                        else:
                            # Si le caractère est déjà pris par un autre joueur
                            test = False
                            for joueur in joueurs.values():
                                if joueur.symbol == msg_recu:
                                    test = True
                            if test is True:
                                msg_envoi = "already_exist"
                            else:
                                identified = True
                                joueurs[client].symbol = msg_recu
                                msg_envoi = "Votre symbole à été paramétré à : {}".format(
                                    joueurs[client].symbol)
                                joueurs[client].step = "sessionInit"

                    """Paramétrage du nom lors de la connection"""
                    if joueurs[client].step == "defName":
                        # Test de la présence ou non d'un pseudo déjà existant parmis les joueurs déjà inscrits
                        test = False
                        for joueur in joueurs.values():
                            if joueur.name == msg_recu:
                                test = True

                        if test is True:
                            msg_envoi = "already_exist"
                        else:
                            joueurs[client].name = msg_recu
                            msg_envoi = "Votre nom à été paramétré à : {}".format(joueurs[client].name)
                            joueurs[client].step = "defSymbol"

                client.send(msg_envoi.encode())
                msg_envoi = ""
                a += 1
# -------------------------------------------------------------------------------------------------------------------- #

########################################################################################################################
#                                                                                                                      #
#                                        Gestion du statut du serveur                                                  #
#                                                                                                                      #
########################################################################################################################

            if winner != "":
                msg_envoi = "|{} gagne, fin de la partie|fin|appuyez sur entree pour sortir|".format(winner)
                client.send(msg_envoi.encode())
            print("Recu : {}".format(msg_recu))
            msg_envoi = ""


print("Fermeture des connexions")

for client in clients_connectes:
    client.close()

connexion_principale.close()
# -------------------------------------------------------------------------------------------------------------------- #
