import unittest

from produto import Produto

class TestProduto(unittest.TestCase):
    def test_create_produto(self):
        produto = Produto('Vassoura', 10)
        self.assertEqual(str(produto), "Nome: Vassoura - Preço: R$ 10.00 - Categoria: Sem categoria - Marcas: Nenhuma marca")

    def test_create_produto_with_negative_price(self):
        with self.assertRaises(ValueError):
            Produto('Vassoura', -10)

    def test_create_produto_with_zero_price(self):
        with self.assertRaises(ValueError):
            Produto('Vassoura', 0)

    def test_registrar_historico(self):
        produto = Produto('Vassoura', 10)
        produto.registrar_historico('Produto criado')
        self.assertEqual(produto.historico, ['Produto criado'])

    def test_alterar_categoria(self):
        produto = Produto('Vassoura', 10)
        produto.alterar_categoria('Limpeza')
        self.assertEqual(produto.categoria, 'Limpeza')
        self.assertEqual(produto.historico, ['Categoria alterada para "Limpeza"'])

    def test_aplica_desconto(self):
        produto = Produto('Vassoura', 10)
        produto.aplicar_desconto(0.1)
        self.assertEqual(produto.preco, 9)
        self.assertEqual(produto.historico, ['Desconto de 10% aplicado. Preço final: R$ 9.00'])

    def test_aplica_desconto_negative(self):
        produto = Produto('Vassoura', 10)
        with self.assertRaises(ValueError):
            produto.aplicar_desconto(-10)

    def test_restaurar_preco(self):
        produto = Produto('Vassoura', 10)
        produto.aplicar_desconto(0.1)
        produto.restaurar_preco(10)
        self.assertEqual(produto.preco, 10)
        self.assertEqual(produto.historico, ['Desconto de 10% aplicado. Preço final: R$ 9.00', 'Preço restaurado para R$ 10.00'])

    def test_add_marca(self):
        produto = Produto('Vassoura', 10)
        produto.set_marca('Marca1')
        self.assertEqual(produto.marca, 'Marca1')
        self.assertEqual(produto.historico, ['Marca Marca1 definida para o produto'])

    def test_remove_marca(self):
        produto = Produto('Vassoura', 10)
        produto.set_marca('Marca1')
        produto.remove_marca()
        self.assertEqual(produto.marca, "Nenhuma marca")
        self.assertEqual(produto.historico, ['Marca Marca1 definida para o produto', 'Marca Marca1 removida do produto'])