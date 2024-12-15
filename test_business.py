import unittest

from business import Business
from produto import Produto

class TestBusiness(unittest.TestCase):
    def test_create_business(self):
        business = Business('Loja de vassouras')
        self.assertEqual(business.nome, "Loja de vassouras")

    def test_create_business_with_empty_name(self):
        with self.assertRaises(ValueError):
            Business('')

    def test_buy_produto_by_produto(self):
        business = Business('Loja de vassouras')
        business.buy_produto(Produto('Vassoura', 10), 10)
        self.assertEqual(business.get_produto_amount('Vassoura'), 10)

    def test_buy_produto_by_name(self):
        business = Business('Loja de vassouras')
        business.buy_produto('Vassoura', 10)
        self.assertEqual(business.get_produto_amount('Vassoura'), 10)

    def test_sell_produto(self):
        business = Business('Loja de vassouras')
        business.buy_produto('Vassoura', 10)
        business.sell_produto('Vassoura', 5)
        self.assertEqual(business.get_produto_amount('Vassoura'), 5)

    def test_sell_produto_insufficient_stock(self):
        business = Business('Loja de vassouras')
        business.buy_produto('Vassoura', 2)
        self.assertFalse(business.sell_produto('Vassoura', 5))

    def test_sell_produto_with_no_stock(self):
        business = Business('Loja de vassouras')
        self.assertFalse(business.sell_produto('Vassoura', 5))