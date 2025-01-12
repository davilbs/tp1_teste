import unittest
from cli import CLI
from io import StringIO
from estoque import Estoque
from produto import Produto
from unittest.mock import Mock

# Testes de integração/e2e da classe CLI
class TestCLIIntegration(unittest.TestCase):
    def setUp(self):
        self.input = StringIO()
        self.output = StringIO()
        self.CLI = CLI(self.input, self.output)

    def tearDown(self):
        del self.input
        del self.output
        del self.CLI
    

    def test_start_mostra_menu_principal(self):
        self.input.writelines([
            "Nome do negócio\n",
            "1\n",
            "\n",
        ])
        self.input.seek(0)

        self.CLI.start()

        saida = self.output.getvalue()
        mensagem = "[MENU PRINCIPAL]"
        self.assertTrue(mensagem in saida)

    def test_start_mostra_tela_adicionar_produtos(self):
        self.input.writelines([
            "Nome do negócio\n",
            "1\n",
            "\n",
            "1\n",
        ])
        self.input.seek(0)

        self.CLI.start()

        saida = self.output.getvalue()
        mensagem = "[ADICIONAR PRODUTOS AO CATÁLOGO]"
        self.assertTrue(mensagem in saida)

    def test_start_mostra_tela_remover_produtos(self):
        self.input.writelines([
            "Nome do negócio\n",
            "1\n",
            "\n",
            "2\n",
        ])
        self.input.seek(0)

        self.CLI.start()

        saida = self.output.getvalue()
        mensagem = "[REMOVER PRODUTOS DO CATÁLOGO]"
        self.assertTrue(mensagem in saida)

    def test_start_mostra_tela_comprar_produtos(self):
        self.input.writelines([
            "Nome do negócio\n",
            "1\n",
            "\n",
            "3\n",
        ])
        self.input.seek(0)

        self.CLI.start()

        saida = self.output.getvalue()
        mensagem = "[COMPRAR PRODUTOS]"
        self.assertTrue(mensagem in saida)

    def test_start_mostra_tela_vender_produtos(self):
        self.input.writelines([
            "Nome do negócio\n",
            "1\n",
            "\n",
            "4\n",
        ])
        self.input.seek(0)

        self.CLI.start()

        saida = self.output.getvalue()
        mensagem = "[VENDER PRODUTOS]"
        self.assertTrue(mensagem in saida)

    def test_start_mostra_tela_consultar_produto(self):
        self.input.writelines([
            "Nome do negócio\n",
            "1\n",
            "\n",
            "5\n",
        ])
        self.input.seek(0)

        self.CLI.start()

        saida = self.output.getvalue()
        mensagem = "[CONSULTAR PRODUTO]"
        self.assertTrue(mensagem in saida)

    def test_start_mostra_tela_exibir_catalogo(self):
        self.input.writelines([
            "Nome do negócio\n",
            "1\n",
            "\n",
            "6\n",
        ])
        self.input.seek(0)

        self.CLI.start()

        saida = self.output.getvalue()
        mensagem = "[CATÁLOGO]"
        self.assertTrue(mensagem in saida)

    
    def test_start_mostra_tela_ajuda(self):
        self.input.writelines([
            "Nome do negócio\n",
            "1\n",
            "\n",
            "7\n",
            "\n",
        ])
        self.input.seek(0)

        self.CLI.start()

        saida = self.output.getvalue()
        mensagem = "[AJUDA - MENU PRINCIPAL]"
        self.assertTrue(mensagem in saida)
    
    def test_start_encerra_se_nao_ler_nome_valido(self):
        self.CLI.start()

        saida = self.output.getvalue()
        mensagem = "Encerrando..."
        self.assertTrue(mensagem in saida)

    def test_start_encerra_se_nao_ler_tipo_estoque_valido(self):
        self.input.writelines([
            "Nome do negócio\n"
        ])
        self.input.seek(0)

        self.CLI.start()

        saida = self.output.getvalue()
        mensagem = "Encerrando..."
        self.assertTrue(mensagem in saida)

    def test_start_adiciona_produtos_mostra_catalogo(self):
        produto = Produto("Produto A", 10.00, "Marca A", "Categoria A")
        self.input.writelines([
            "Nome do negócio\n",
            "1\n",
            "\n",
            "1\n",
            "Produto A\n",
            "Marca A\n",
            "Categoria A\n",
            "10.00\n",
            "6\n"
        ])
        self.input.seek(0)

        self.CLI.start()

        saida = self.output.getvalue()
        self.assertTrue("Produto adicionado com sucesso!" in saida)
        self.assertTrue(f"- {produto}" in saida)

    def test_start_mostra_catalogo_vazio(self):
        self.input.writelines([
            "Nome do negócio\n",
            "1\n",
            "\n",
            "6\n",
            "\n",
        ])
        self.input.seek(0)

        self.CLI.start()

        saida = self.output.getvalue()
        self.assertTrue("O catálogo está vazio." in saida)

