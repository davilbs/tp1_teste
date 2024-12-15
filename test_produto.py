import unittest

from produto import Produto

class TestProduto(unittest.TestCase):
    def test_create_produto(self):
        produto = Produto('Vassoura', 10)
        self.assertEqual(str(produto), "Vassoura - R$ 10.00 - Categoria: Sem categoria - Marcas: Nenhuma marca")

    def test_create_produto_with_negative_price(self):
        with self.assertRaises(ValueError):
            Produto('Vassoura', -10)

    def test_create_produto_with_zero_price(self):
        with self.assertRaises(ValueError):
            Produto('Vassoura', 0)

