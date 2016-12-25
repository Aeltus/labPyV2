# -*-coding:Latin-1 -*

from lib.player import *
from lib.files import *

"""Contient toutes les caratéristiques et méthodes de la carte choisie pour jouer"""

class Map:

    def __init__(self):

        self._dic = {}

    def _set_dic(self, dic):
        self._dic = dic

    def _get_dic(self):
        return self._dic

    dic = property(_get_dic, _set_dic)

    """Crée un dictionnaire de carte depuis un fichier txt"""
    def creator(self, origin, map):

        content = Files.fopen(origin+map)
        x = y = 0
        for (i, symbol) in enumerate(content):
            localisation = (x, y)
            self._dic[localisation] = symbol

            x += 1

            if symbol == "\n":
                y += 1
                x = 0



    """Récupère un dictionnaire de carte"""
    def recuperator(self, origin, map):
        self._dic = Files.dic_recuperator(origin, map)


    """Sauvegarde un dictionnaire de carte"""
    def saver(self, origin, map):
        Files.dic_saver(origin, map, self._dic)



    """Affiche à l'écran un dictionnaire de carte"""
    def display(self, player):
        contentLine = ""
        x = y = 0
        while True:
            location = (x, y)
            if location in self._dic:
                contentLine = "{}{}".format(contentLine, self._dic[location])

                if self._dic[location] == "X":
                    player.x = x
                    player.y = y
                x += 1
            else:
                print(contentLine[0:-1])
                contentLine = ""
                y += 1
                x = 0
                location = (x, y)
                if location not in self._dic:
                    break

    """Teste si le mouvement est possible et détermine la nouvelle position du joueur ainsi que s'il a gagné ou non"""
    def mouvement_try(self, direction, vitesse, player):

        mur = win = False
        l = 0

        if direction == "n":

            while l < int(vitesse):

                l += 1
                location = (player.x, player.y - l)
                if self._dic[location] == "O":
                    mur = True
                    break
                if self._dic[location] == "U":
                    win = True
                    break

        if direction == "s":

            while l < int(vitesse):

                l += 1
                location = (player.x, player.y + l)
                if self._dic[location] == "O":
                    mur = True
                    break
                if self._dic[location] == "U":
                    win = True
                    break

        if direction == "e":

            while l < int(vitesse):

                l += 1
                location = (player.x + l, player.y)
                if self._dic[location] == "O":
                    mur = True
                    break
                if self._dic[location] == "U":
                    win = True
                    break

        if direction == "o":

            while l < int(vitesse):

                l += 1
                location = (player.x - l, player.y)
                if self._dic[location] == "O":
                    mur = True
                    break
                if self._dic[location] == "U":
                    win = True
                    break

        return mur, win, location
