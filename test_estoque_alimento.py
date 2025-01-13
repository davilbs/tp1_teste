import unittest

from estoque import EstoqueAlimento
from produto import ProdutoAlimento

class TestEstoqueAlimento(unittest.TestCase):
    def test_add_one_product(self):
        estoque = EstoqueAlimento("Loja de Arroz")
        estoque.add_produto(ProdutoAlimento('Arroz', 10))
        self.assertEqual(str(estoque.get_produto_info('Arroz')), "Arroz - R$ 10.00")

    def test_add_one_product_alimento(self):
        estoque = EstoqueAlimento("Loja de Arroz")
        estoque.add_produto(ProdutoAlimento('Arroz', 10, validade='2021-12-31'))
        self.assertEqual(str(estoque.get_produto_info('Arroz')), "Arroz - R$ 10.00 - 2021-12-31")