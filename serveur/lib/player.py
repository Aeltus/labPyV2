# -*-coding:Utf-8 -*

"""
Définition d'une classe player
reprenant ces coordonnées
"""


class Player:
    def __init__(self):
        """

        Instance de joueur contenant ces coordonnées, son symbole et son nom

        """
        self._x = 0
        self._y = 0
        self._symbol = ""
        self._name = ""
        self._tour = 0
        self._ready = False
        self._requette = ""
        self._step = "defName"

    def _get_x(self):
        return self._x

    def _get_y(self):
        return self._y

    def _get_symbol(self):
        return self._symbol

    def _get_name(self):
        return self._name

    def _get_tour(self):
        return self._tour

    def _get_ready(self):
        return self._ready

    def _get_requette(self):
        return self._requette

    def _get_step(self):
        return self._step

    def _set_x(self, value):
        self._x = value

    def _set_y(self, value):
        self._y = value

    def _set_symbol(self, value):
        self._symbol = value

    def _set_name(self, value):
        self._name = value

    def _set_tour(self, value):
        self._tour = value

    def _set_ready(self, value):
        self._ready = value

    def _set_requette(self, value):
        self._requette = value

    def _set_step(self, value):
        self._step = value

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)
    symbol = property(_get_symbol, _set_symbol)
    name = property(_get_name, _set_name)
    tour = property(_get_tour, _set_tour)
    ready = property(_get_ready, _set_ready)
    requette = property(_get_requette, _set_requette)
    step = property(_get_step, _set_step)
