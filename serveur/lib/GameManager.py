# -*-coding:Utf-8 -*

from lib.compartment import Compartment
from lib.player import Player
from random import randrange


class GameManager:
    def game_init(joueurs, data, max_x, max_y):
        """Démarage de la session, avant que le jeu ne commence, on positionne les joueurs sur la grille"""
        i = 0
        for joueur in joueurs.values():
            """le premier joueur prend le premier tour"""
            if i == 0:
                joueur.tour = 1
                i += 1
            while True:
                loc_x = randrange(0, max_x)
                loc_y = randrange(0, max_y + 1)
                loc_x_y = (loc_x, loc_y)
                if data[loc_x_y].content in [".", " "]:
                    data[loc_x_y].visible = joueur.symbol
                    joueur.x = loc_x
                    joueur.y = loc_y
                    break
        return joueurs, data
    game_init = staticmethod(game_init)

    def session_init(paquet, joueurs, client):
        test = True
        msg_envoi = ""
        if paquet == "status" and joueurs[client].ready is False:
            msg_envoi = "Envoyez c pour indiquer que vous etes pret, le jeu debutera quand tout le monde sera pret."
            joueurs[client].step = "sessionInit"
            test = False
        elif paquet == "c":
            joueurs[client].ready = True
            msg_envoi = "|La partie demarrera quand tout le monde sera pret.|"
            joueurs[client].step = "gameInit"
            for joueur in joueurs.values():
                if joueur.ready is False:
                    test = False
        return msg_envoi, test, joueurs
    session_init = staticmethod(session_init)

    def joueur_suivant(joueurs):
        """
        Passe au joueur suivant :

        :param joueurs

        reçoit un tableau d'objets de type joueurs
        renvoi le même tableau mis à jour sur le joueur suivant

        """
        nbre_joueurs = len(joueurs)
        if nbre_joueurs > 1:
            tour_joueur_numero = 0
            i = 1
            for joueur in joueurs.values():
                if joueur.tour == 1:
                    tour_joueur_numero = i
                    joueur.tour = 0
                i += 1
            if tour_joueur_numero == nbre_joueurs:
                tour_joueur_numero = 1
            else:
                tour_joueur_numero += 1

            i = 1
            for joueur in joueurs.values():
                if i == tour_joueur_numero:
                    joueur.tour = 1
                i += 1

            return joueurs
    joueur_suivant = staticmethod(joueur_suivant)

    def request_analyser(requette):
        """

        Prend une requette et la renvoie sous forme standard ordre, et direction

        :param requette:
        :return:

        """
        ordre = ""
        direction = ""
        vitesse = 0

        if requette[0] in ["n", "s", "e", "o"]:
            ordre = "a"
            direction = requette[0]
            if len(requette) > 1:
                if requette[1] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    vitesse = requette[1:]
            else:
                vitesse = 1
        elif requette[0] in ["m", "p"] and requette[1] in ["n", "s", "e", "o"]:
            ordre = requette[0]
            direction = requette[1]

        return ordre, direction, vitesse

    request_analyser = staticmethod(request_analyser)
