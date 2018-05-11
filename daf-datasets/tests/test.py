import unittest
from daf.datasets.regione_toscana import atti_dirigenti


class AttiDirigentiTests(unittest.TestCase):

    def test_get_label_index(self):
        label_index = atti_dirigenti.get_label_index()
        self.assertTrue(len(label_index) > 0)

    def test_load_data(self):
        (x_train, y_train), (x_test, y_test) = atti_dirigenti.load_data()
        self.assertTrue(len(x_train) == len(y_train))

    def test_load_word_index(self):
        word_index = atti_dirigenti.get_word_index()
        self.assertTrue(len(word_index) > 0)


if __name__ == '__main__':
    unittest.main()