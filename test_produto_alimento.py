import unittest

from produto import ProdutoAlimento

class TestProdutoAlimento(unittest.TestCase):
    def test_create_produto_alimento(self):
        produto = ProdutoAlimento('Vassoura', 10, validade='2021-12-31')
        self.assertEqual(str(produto), "Vassoura - R$ 10.00 - 2021-12-31")

    def test_create_produto_alimento_vegano(self):
        produto = ProdutoAlimento('Vassoura', 10, vegano=True)
        self.assertEqual(str(produto), "Vassoura - R$ 10.00 vegano")
    
    def test_set_valdade(self):
        produto = ProdutoAlimento('Vassoura', 10)
        produto.set_validade('2021-12-31')
        self.assertEqual(str(produto), "Vassoura - R$ 10.00 - 2021-12-31")

    def test_set_vegano(self):
        produto = ProdutoAlimento('Vassoura', 10)
        produto.set_vegano(True)
        self.assertEqual(str(produto), "Vassoura - R$ 10.00 vegano")