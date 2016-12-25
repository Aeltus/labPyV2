# -*-coding:Latin-1 -*

"""
Définition d'une classe player
reprenant ces coordonnées
"""


class Player:
    def __init__(self):
        self._x = 0
        self._y = 0

    def _get_x(self):
        return self._x

    def _get_y(self):
        return self._y

    def _set_x(self, value):
        self._x = value

    def _set_y(self, value):
        self._y = value

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)
