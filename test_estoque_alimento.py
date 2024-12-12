import unittest

from estoque import EstoqueAlimento
from produto import ProdutoAlimento

class TestEstoqueAlimento(unittest.TestCase):
    def test_add_one_product(self):
        estoque = EstoqueAlimento()
        estoque.add_produto(ProdutoAlimento('Arroz', 10))
        self.assertEqual(str(estoque.get_produto_info('Arroz')), "Arroz - R$ 10.00")

    def test_add_one_product_alimento(self):
        estoque = EstoqueAlimento()
        estoque.add_produto(ProdutoAlimento('Arroz', 10, validade='2021-12-31'))
        self.assertEqual(str(estoque.get_produto_info('Arroz')), "Arroz - R$ 10.00 - 2021-12-31")

    def test_remove_vencidos(self):
        estoque = EstoqueAlimento()
        estoque.add_produto(ProdutoAlimento('Arroz', 10, validade='2021-12-31'))
        estoque.add_produto(ProdutoAlimento('Feijao', 10, validade='2021-12-31'))
        estoque.add_produto(ProdutoAlimento('Milho', 10, validade='2021-12-31'))
        estoque.remove_vencidos('2022-01-01')
        self.assertEqual(estoque.get_produto_info('Arroz'), None)
        self.assertEqual(estoque.get_produto_info('Feijao'), None)
        self.assertEqual(estoque.get_produto_info('Milho'), None)