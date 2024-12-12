import unittest

from estoque import Estoque
from produto import Produto
class TestEstoque(unittest.TestCase):
    def test_buy_one_product(self):
        estoque = Estoque()
        estoque.buy_produto('Vassoura', 10)
        self.assertEqual(estoque.get_produto_amount('Vassoura'), 10)

    def test_add_one_product(self):
        estoque = Estoque()
        estoque.add_produto(Produto('Vassoura', 10))
        self.assertEqual(str(estoque.get_produto_info('Vassoura')), "Vassoura - R$ 10.00")