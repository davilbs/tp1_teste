import unittest

from business import Business
from produto import Produto
from estoque import Estoque
from database import create_database

class TestBusiness(unittest.TestCase):
    def setUp(self):
        create_database()
    
    def test_create_business(self):
        business = Business("Loja de vassouras")
        self.assertEqual(business.nome, "Loja_de_vassouras")

    def test_buy_produto_by_produto(self):
        business = Business('Loja de vassouras')
        produto = Produto('Vassoura', 10)
        business.buy_produto(produto, 10)
        self.assertEqual(business.get_produto_amount('Vassoura'), 10)

    def test_buy_produto_by_name(self):
        business = Business('Loja de vassouras')
        produto = Produto('Vassoura', 10)
        business.buy_produto(produto, 10)
        business.buy_produto('Vassoura', 10)
        self.assertEqual(business.get_produto_amount('Vassoura'), 20)

    def test_sell_produto(self):
        business = Business('Loja de vassouras')
        produto = Produto('Vassoura', 10)
        business.buy_produto(produto, 10)
        business.sell_produto("1", 5)
        self.assertEqual(business.get_produto_amount('Vassoura'), 5)

    def test_sell_produto_insufficient_stock(self):
        business = Business('Loja de vassouras')
        produto = Produto('Vassoura', 10)
        business.buy_produto(produto, 2)
        self.assertFalse(business.sell_produto("1", 5))

    def test_sell_produto_with_no_stock(self):
        business = Business('Loja de vassouras')
        self.assertFalse(business.sell_produto('1', 5))

    def test_calculate_profit(self):
        business = Business('Loja de vassouras')
        produto = Produto('Vassoura', 10)
        business.buy_produto(produto, 10)
        business.sell_produto("1", 5)
        self.assertEqual(business.calculate_profit(), 50.0)

    def test_set_desconto(self):
        business = Business('Loja de vassouras')
        business.set_desconto(10)
        self.assertEqual(business.desconto, 10)

    def test_set_desconto_invalid(self):
        business = Business('Loja de vassouras')
        with self.assertRaises(ValueError):
            business.set_desconto(-10)
    
    def test_alterar_nome(self):
        business = Business("Loja de vassouras")
        business.alterar_nome("Loja de vassouras LTDA")
        self.assertEqual(business.nome, "Loja_de_vassouras_LTDA")

    def test_alterar_nome_invalid(self):
        business = Business('Loja de vassouras')
        with self.assertRaises(ValueError):
            business.alterar_nome('')

    def test_listar_estoque(self):
        business = Business('Loja de vassouras')
        produto = Produto('Vassoura', 10)
        business.buy_produto(produto, 10)
        self.assertEqual(str(business.listar_estoque()), str(['ID 1 - Nome: Vassoura - Preço: R$ 10.00 - Categoria: Sem categoria - Marcas: Nenhuma marca']))