import unittest

from estoque import EstoqueAlimento

class TestEstoque(unittest.TestCase):
    def test_add_one_product(self):
        estoque = EstoqueAlimento()
        estoque.buy_alimento('arroz', 10)
        self.assertEqual(estoque.get_alimento('arroz'), 10)