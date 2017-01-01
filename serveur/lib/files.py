# -*-coding:Utf-8 -*
"""contient les méthodes d'accès aux fichiers"""

class Files:

    def fopen(path):
        """récupère les données d'un fichier situé à l'adresse path"""
        file = open(path, 'r')
        content = file.read()
        file.close()
        return content
    fopen = staticmethod(fopen)
