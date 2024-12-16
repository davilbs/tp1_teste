import unittest

from business import Business
from produto import Produto
from estoque import Estoque

class TestBusiness(unittest.TestCase):
    def test_create_business(self):
        business = Business('Loja de vassouras', estoque=Estoque())
        self.assertEqual(business.nome, "Loja de vassouras")

    def test_buy_produto_by_produto(self):
        business = Business('Loja de vassouras', estoque=Estoque())
        produto = Produto('Vassoura', 10)
        business.buy_produto(produto, 10)
        self.assertEqual(business.get_produto_amount('Vassoura'), 10)

    def test_buy_produto_by_name(self):
        business = Business('Loja de vassouras', estoque=Estoque())
        produto = Produto('Vassoura', 10)
        business.buy_produto(produto, 10)
        business.buy_produto('Vassoura', 10)
        self.assertEqual(business.get_produto_amount('Vassoura'), 20)

    def test_sell_produto(self):
        business = Business('Loja de vassouras', estoque=Estoque())
        produto = Produto('Vassoura', 10)
        business.buy_produto(produto, 10)
        business.sell_produto('Vassoura', 5)
        self.assertEqual(business.get_produto_amount('Vassoura'), 5)

    def test_sell_produto_insufficient_stock(self):
        business = Business('Loja de vassouras', estoque=Estoque())
        produto = Produto('Vassoura', 10)
        business.buy_produto(produto, 2)
        self.assertFalse(business.sell_produto('Vassoura', 5))

    def test_sell_produto_with_no_stock(self):
        business = Business('Loja de vassouras', estoque=Estoque())
        self.assertFalse(business.sell_produto('Vassoura', 5))

    def test_calculate_profit(self):
        business = Business('Loja de vassouras', estoque=Estoque())
        produto = Produto('Vassoura', 10)
        business.buy_produto(produto, 10)
        business.sell_produto('Vassoura', 5)
        self.assertEqual(business.calculate_profit(), -40)

    def test_set_desconto(self):
        business = Business('Loja de vassouras', estoque=Estoque())
        business.set_desconto(10)
        self.assertEqual(business.desconto, 10)

    def test_set_desconto_invalid(self):
        business = Business('Loja de vassouras', estoque=Estoque())
        with self.assertRaises(ValueError):
            business.set_desconto(-10)
    
    def test_alterar_nome(self):
        business = Business('Loja de vassouras', estoque=Estoque())
        business.alterar_nome('Loja de vassouras LTDA')
        self.assertEqual(business.nome, 'Loja de vassouras LTDA')

    def test_alterar_nome_invalid(self):
        business = Business('Loja de vassouras', estoque=Estoque())
        with self.assertRaises(ValueError):
            business.alterar_nome('')

    def test_listar_estoque(self):
        business = Business('Loja de vassouras', estoque=Estoque())
        produto = Produto('Vassoura', 10)
        business.buy_produto(produto, 10)
        self.assertEqual(business.listar_estoque(), ['Vassoura - R$ 10.00 - Categoria: Sem categoria - Marcas: Nenhuma marca'])