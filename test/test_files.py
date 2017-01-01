from serveur.lib.files import Files
import unittest


class FilesTest(unittest.TestCase):

    def test_files(self):
        elt = Files.fopen("serveur/dic/maps/facile.txt")
        self.assertIsNotNone(elt)
