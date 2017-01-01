# -*-coding:Utf-8 -*

from lib.compartment import Compartment


class MapManager:
    def get_string_map_from_dic(dic):

        content_map = ""
        x = y = 0
        while True:

            location = (x, y)

            if location in dic:
                content_map = "{}{}".format(content_map, dic[location].visible)
                x += 1

            else:

                y += 1
                x = 0
                location = (x, y)
                if location not in dic:
                    break

        return content_map

    get_string_map_from_dic = staticmethod(get_string_map_from_dic)

    def map_initialiser(content):
        data = {}
        x = y = i = 0
        while i < len(content):
            localisation = (x, y)
            data[localisation] = Compartment(content[i], content[i])

            x += 1

            if content[i] == "\n":
                y += 1
                x = 0

            i += 1

        return data, x, y
    map_initialiser = staticmethod(map_initialiser)
