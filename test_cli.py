import unittest
from cli import CLI
from io import StringIO

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.input = StringIO()
        self.output = StringIO()
        self.CLI = CLI(self.input, self.output)

    def test_tela_escolher_estoque_generico(self):
        self.input.write("1\n")
        self.input.seek(0)

        tipo = self.CLI.tela_escolher_tipo_estoque()

        saida = self.output.getvalue()
        self.assertEqual(tipo, 1)
        self.assertGreater(saida.find("Tipo escolhido: Estoque Genérico"), -1)

    def test_tela_escolher_estoque_alimentos(self):
        self.input.write("2\n")
        self.input.seek(0)

        tipo = self.CLI.tela_escolher_tipo_estoque()
        saida = self.output.getvalue()

        self.assertEqual(tipo, 2)
        self.assertGreater(saida.find("Tipo escolhido: Estoque de alimentos"), -1)

    def test_tela_escolher_estoque_opcao_invalida(self):

        self.input.write("5\n1\n")
        self.input.seek(0)

        self.CLI.tela_escolher_tipo_estoque()

        saida = self.output.getvalue()
        self.assertGreater(saida.find("Opção inválida. Por favor, escolha uma das opções disponíveis."), -1)
    
    def test_handle_criacao_estoque_generico(self):
        self.CLI.handle_criacao_estoque(1)
        self.assertFalse(self.CLI.is_estoque_alimento)

    def test_handle_criacao_estoque_alimentos(self):
        self.CLI.handle_criacao_estoque(2)
        self.assertTrue(self.CLI.is_estoque_alimento)

    def test_handle_criacao_estoque_valor_invalido(self):
        with self.assertRaises(Exception):
            self.CLI.handle_criacao_estoque(5)
    
    def test_tela_consultar_produto_inexistente(self):
        self.input.write("Arroz\n")
        self.input.seek(0)

        self.CLI.handle_criacao_estoque(1)
        self.CLI.tela_consultar_produto()


        saida = self.output.getvalue()
        self.assertGreater(saida.find("O produto procurado não existe no catálogo."), -1)
    
    def test_tela_info_funcionamento(self):
        self.input.write("\n")
        self.input.seek(0)

        self.CLI.tela_info_funcionamento()

        saida = self.output.getvalue()
        self.assertGreater(saida.find("FUNCIONAMENTO DO SISTEMA"), -1)

    def test_tela_ajuda_menu_principal(self):
        self.input.write("\n")
        self.input.seek(0)

        self.CLI.tela_ajuda_menu_principal()

        saida = self.output.getvalue()
        self.assertGreater(saida.find("AJUDA - MENU PRINCIPAL"), -1)
    
    def test_tela_exibir_catalogo_vazio(self):
        self.CLI.tela_exibir_catalogo()
        saida = self.output.getvalue()
        self.assertGreater(saida.find("O catálogo está vazio"), -1)


