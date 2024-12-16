import unittest

from estoque import Estoque
from produto import Produto
class TestEstoque(unittest.TestCase):
    def test_buy_one_product(self):
        estoque = Estoque()
        produto = Produto('Vassoura', 10)
        estoque.buy_produto(produto, 10)
        self.assertEqual(estoque.get_produto_amount('Vassoura'), 10)

    def test_add_one_product(self):
        estoque = Estoque()
        estoque.add_produto(Produto('Vassoura', 10))
        self.assertEqual(str(estoque.get_produto_info('Vassoura')), "Vassoura - R$ 10.00 - Categoria: Sem categoria - Marcas: Nenhuma marca")

    def test_remove_one_product(self):
        estoque = Estoque()
        estoque.add_produto(Produto('Vassoura', 10))
        estoque.remove_produto(Produto('Vassoura', 10))
        self.assertEqual(estoque.get_produto_info('Vassoura'), None)

    def test_sell_one_product(self):
        estoque = Estoque()
        estoque.add_produto(Produto('Vassoura', 10))
        estoque.buy_produto('Vassoura', 10)
        estoque.sell_produto('Vassoura', 5)
        self.assertEqual(estoque.get_produto_amount('Vassoura'), 5)

    def test_sell_one_product_insufficient_stock(self):
        estoque = Estoque()
        estoque.add_produto(Produto('Vassoura', 10))
        estoque.buy_produto('Vassoura', 2)
        self.assertFalse(estoque.sell_produto('Vassoura', 5))

    def test_sell_one_product_with_no_stock(self):
        estoque = Estoque()
        estoque.add_produto(Produto('Vassoura', 10))
        self.assertFalse(estoque.sell_produto('Vassoura', 5))

    def test_get_estoque_size(self):
        estoque = Estoque()
        estoque.add_produto(Produto('Vassoura', 10))
        estoque.add_produto(Produto('Pá', 10))
        estoque.buy_produto('Vassoura', 10)
        estoque.buy_produto('Pá', 5)
        self.assertEqual(estoque.get_estoque_size(), 15)

    def test_get_estoque(self):
        estoque = Estoque()
        vassoura = Produto('Vassoura', 10)
        pa = Produto('Pá', 10)
        estoque.add_produto(vassoura)
        estoque.add_produto(pa)
        estoque.buy_produto('Vassoura', 10)
        estoque.buy_produto('Pá', 5)
        self.assertEqual(estoque.get_estoque(), [vassoura, pa])