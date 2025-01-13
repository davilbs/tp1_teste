import unittest

from estoque import Estoque
from produto import Produto
from database import create_database
class TestEstoque(unittest.TestCase):
    def setUp(self):
        create_database()
    
    def test_buy_one_product(self):
        estoque = Estoque("Loja de Vassouras")
        produto = Produto('Vassoura', 10)
        added_produto = estoque.add_produto(produto)
        estoque.buy_produto(added_produto, 10)
        self.assertEqual(estoque.get_produto_amount('Vassoura'), 10)

    def test_add_one_product(self):
        estoque = Estoque("Loja de Vassouras")
        added_produto = estoque.add_produto(Produto('Vassoura', 10))
        self.assertEqual(str(estoque.get_produto_info(str(added_produto.id))), "ID 1 - Nome: Vassoura - Preço: R$ 10.00 - Categoria: Sem categoria - Marcas: Nenhuma marca")

    def test_remove_one_product(self):
        estoque = Estoque("Loja de Vassouras")
        estoque.add_produto(Produto('Vassoura', 10))
        estoque.remove_produto(Produto('Vassoura', 10, id=1))
        self.assertEqual(estoque.get_produto_info('Vassoura'), None)

    def test_sell_one_product(self):
        estoque = Estoque("Loja de Vassouras")
        added_produto = estoque.add_produto(Produto('Vassoura', 10))
        estoque.buy_produto(added_produto, 10)
        estoque.sell_produto(str(added_produto.id), 5)
        self.assertEqual(estoque.get_produto_amount('Vassoura'), 5)

    def test_sell_one_product_insufficient_stock(self):
        estoque = Estoque("Loja de Vassouras")
        added_produto = estoque.add_produto(Produto('Vassoura', 10))
        estoque.buy_produto(str(added_produto.id), 2)
        self.assertFalse(estoque.sell_produto(str(added_produto.id), 5))

    def test_sell_one_product_with_no_stock(self):
        estoque = Estoque("Loja de Vassouras")
        added_produto = estoque.add_produto(Produto('Vassoura', 10))
        self.assertFalse(estoque.sell_produto(str(added_produto.id), 5))

    def test_get_estoque_size(self):
        estoque = Estoque("Loja de Vassouras")
        added_produto1 = estoque.add_produto(Produto('Vassoura', 10))
        added_produto2 = estoque.add_produto(Produto('Pá', 10))
        estoque.buy_produto(added_produto1, 10)
        estoque.buy_produto(added_produto2, 5)
        self.assertEqual(estoque.get_estoque_size(), 15)

    def test_get_estoque(self):
        estoque = Estoque("Loja de Vassouras")
        vassoura = Produto('Vassoura', 10)
        pa = Produto('Pá', 10)
        added_produto1 = estoque.add_produto(vassoura)
        added_produto2 = estoque.add_produto(pa)
        estoque.buy_produto(added_produto1, 10)
        estoque.buy_produto(added_produto2, 5)
        self.assertEqual(str(estoque.get_estoque()), str([added_produto1, added_produto2]))