"""contient les méthodes d'accès aux fichiers"""

import pickle

class Files:

    def fopen(path):
        file = open(path, 'r')
        content = file.read()
        file.close()
        return content
    fopen = staticmethod(fopen)

    def dic_saver(origin, map, dictionnary):
        with open(origin+map, 'wb') as fichier:
            mon_pickler = pickle.Pickler(fichier)
            mon_pickler.dump(dictionnary)

    dic_saver = staticmethod(dic_saver)

    def dic_recuperator(origin, map):
        with open(origin+map, 'rb') as fichier:
            mon_depickler = pickle.Unpickler(fichier)
            return mon_depickler.load()
    dic_recuperator = staticmethod(dic_recuperator)