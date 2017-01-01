# -*-coding:Utf-8 -*

"""Classe contenant les informations relatives à une case du jeu"""


class Compartment:
    def __init__(self, content, visible):
        """
        Crée une instance d'une case du jeu

        :param content:
        :param visible:

        """
        self._visible = visible
        self._content = content

    def _get_visible(self):
        return self._visible

    def _set_visible(self, visible):
        self._visible = visible

    def _get_content(self):
        return self._content

    def _set_content(self, value):
        self._content = value

    visible = property(_get_visible, _set_visible)
    content = property(_get_content, _set_content)
