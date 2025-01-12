import unittest
from cli import CLI
from io import StringIO
from estoque import Estoque
from produto import Produto
from unittest.mock import Mock

# Testes de unidade da classe CLI
class TestCLI(unittest.TestCase):
    def setUp(self):
        self.input = StringIO()
        self.output = StringIO()
        self.CLI = CLI(self.input, self.output)

    def tearDown(self):
        del self.input
        del self.output
        del self.CLI

    def test_cli_no_atty(self):
        self.assertFalse(self.CLI._atty)

    def test_start_encerra_corretamente_com_ctrl_c(self):
        self.CLI.tela_escolher_nome = Mock(side_effect=KeyboardInterrupt)

        self.CLI.start()

        saida = self.output.getvalue()
        mensagem = "Encerrando..."
        self.assertTrue(mensagem in saida)

    def test_start_encerra_corretamente_com_eof(self):
        self.CLI.start()

        saida = self.output.getvalue()
        mensagem = "Encerrando..."
        self.assertTrue(mensagem in saida)

    def test_start_encerra_corretamente_com_excecao(self):
        self.CLI.tela_escolher_nome = Mock(side_effect=Exception)

        self.CLI.start()

        saida = self.output.getvalue()
        mensagem = "Encerrando..."
        self.assertTrue(mensagem in saida)

    def test_tela_escolher_nome_valido(self):
        nome_teste = "Nome de teste"
        self.input.write(nome_teste + "\n")
        self.input.seek(0)

        nome = self.CLI.tela_escolher_nome()

        saida = self.output.getvalue()
        self.assertEqual(nome, nome_teste)
        self.assertEqual(saida.find("O nome do negócio não pode ficar vazio"), -1)
    
    def test_tela_escolher_nome_vazio(self):
        self.input.write("\n")
        self.input.seek(0)

        nome = self.CLI.tela_escolher_nome()

        saida = self.output.getvalue()
        mensagem = "O nome do negócio não pode ficar vazio"
        self.assertTrue(mensagem in saida)
        self.assertIsNone(nome)

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
        self.input.write("5\n")
        self.input.seek(0)

        tipo = self.CLI.tela_escolher_tipo_estoque()

        saida = self.output.getvalue()
        mensagem = "Opção inválida. Por favor, escolha uma das opções disponíveis."
        self.assertTrue(mensagem in saida)
        self.assertIsNone(tipo)
    
    def test_handle_criacao_estoque_generico(self):
        self.CLI.handle_criacao_estoque(1)
        self.assertFalse(self.CLI.is_estoque_alimento)

    def test_handle_criacao_estoque_alimentos(self):
        self.CLI.handle_criacao_estoque(2)
        self.assertTrue(self.CLI.is_estoque_alimento)

    def test_handle_criacao_estoque_valor_invalido(self):
        with self.assertRaises(Exception):
            self.CLI.handle_criacao_estoque(5)

    def test_tela_info_funcionamento(self):
        self.input.write("\n")
        self.input.seek(0)

        self.CLI.tela_info_funcionamento()

        saida = self.output.getvalue()
        self.assertGreater(saida.find("FUNCIONAMENTO DO SISTEMA"), -1)

    def test_tela_menu_principal(self):
        opcao = 1
        self.input.write(f"{opcao}\n")
        self.input.seek(0)
        
        res = self.CLI.tela_menu_principal()
        self.assertEqual(res, opcao)

    def test_tela_menu_principal_opcao_invalida(self):
        self.input.write("9\n")
        self.input.seek(0)
        
        with self.assertRaises(EOFError):
            self.CLI.tela_menu_principal()

        saida = self.output.getvalue()
        self.assertGreater(saida.find("Opção inválida. Por favor, escolha uma das opções disponíveis."), -1)

    def test_tela_adicionar_produtos(self):
        self.input.writelines([
            "Produto A\n",
            "Marca A\n",
            "Categoria A\n",
            "10.00\n"
        ])
        self.input.seek(0)

        self.CLI.tela_adicionar_produtos()

        saida = self.output.getvalue()
        mensagem = "Produto adicionado com sucesso!"
        self.assertTrue(mensagem in saida)

    def test_tela_adicionar_produtos_nome_vazio(self):
        self.input.write("\n")
        self.input.seek(0)

        with self.assertRaises(ValueError) as cm:
            self.CLI.tela_adicionar_produtos()
        
        mensagem = "O nome do produto não pode ser vazio"
        self.assertTrue(mensagem in cm.exception.args)

    def test_tela_adicionar_produtos_marca_vazia(self):
        self.input.writelines([
            "Produto A\n",
            "\n"
        ])
        self.input.seek(0)

        with self.assertRaises(ValueError) as cm:
            self.CLI.tela_adicionar_produtos()
        
        mensagem = "A marca do produto não pode ser vazia"
        self.assertTrue(mensagem in cm.exception.args)

    def test_tela_adicionar_produtos_categoria_vazia(self):
        self.input.writelines([
            "Produto A\n",
            "Marca A\n",
            "\n"
        ])
        self.input.seek(0)

        with self.assertRaises(ValueError) as cm:
            self.CLI.tela_adicionar_produtos()
        
        mensagem = "A categoria do produto não pode ser vazia"
        self.assertTrue(mensagem in cm.exception.args)

    def test_tela_adicionar_produtos_preco_vazia(self):
        self.input.writelines([
            "Produto A\n",
            "Marca A\n",
            "Categoria A\n",
            "\n"
        ])
        self.input.seek(0)

        with self.assertRaises(ValueError) as cm:
            self.CLI.tela_adicionar_produtos()
        
        mensagem = "O preço do produto não pode ser vazio"
        self.assertTrue(mensagem in cm.exception.args)

    def test_tela_adicionar_produtos_erro(self):
        self.input.writelines([
            "Produto A\n",
            "Marca A\n",
            "Categoria A\n",
            "10.00\n"
        ])
        self.input.seek(0)
        self.CLI.business.buy_produto = Mock(return_value=False)

        self.CLI.tela_adicionar_produtos()

        saida = self.output.getvalue()
        mensagem = "[ERRO] Houve um erro ao adicionar o produto ao estoque."
        self.assertTrue(mensagem in saida)

    def test_tela_remover_produtos(self):
        produto = Produto("Produto A", 10.00, "Marca A", "Categoria A")
        self.CLI.business.get_produto_info = Mock(return_value=produto)
        self.CLI.business.remove_produto = Mock(return_value=True)
        self.input.write("Produto A\n")
        self.input.seek(0)

        self.CLI.tela_remover_produtos()
        
        saida = self.output.getvalue()
        mensagem = "Produto removido com sucesso"
        self.assertTrue(mensagem in saida)

    def test_tela_remover_produtos_nome_vazio(self):
        self.input.write("\n")
        self.input.seek(0)

        with self.assertRaises(ValueError) as cm:
            self.CLI.tela_remover_produtos()
        
        mensagem = "O nome do produto não pode ser vazio"
        self.assertTrue(mensagem in cm.exception.args)

    def test_tela_remover_produtos_inexistente(self):
        self.input.writelines([
            "Produto A\n",
        ])
        self.input.seek(0)

        self.CLI.tela_remover_produtos()

        saida = self.output.getvalue()
        mensagem = "[ERRO] O produto não existe no estoque."
        self.assertTrue(mensagem in saida)

    def test_tela_remover_produtos_erro(self):
        produto = Produto("Produto A", 10.00, "Marca A", "Categoria A")
        self.CLI.business.get_produto_info = Mock(return_value=produto)
        self.CLI.business.remove_produto = Mock(return_value=False)
        self.input.writelines("Produto A\n")
        self.input.seek(0)
        self.CLI.business.buy_produto = Mock(return_value=False)

        self.CLI.tela_remover_produtos()

        saida = self.output.getvalue()
        mensagem = "[ERRO] Houve um erro ao remover o produto do catálogo"
        self.assertTrue(mensagem in saida)

    def test_tela_comprar_produtos(self):
        produto = Produto("Produto A", 10.00, "Marca A", "Categoria A")
        self.CLI.business.get_produto_info = Mock(return_value=produto)
        self.CLI.business.buy_produto = Mock(return_value=True)
        self.input.writelines([
            "Produto A\n",
            "10\n"
        ])
        self.input.seek(0)

        self.CLI.tela_comprar_produtos()
        
        saida = self.output.getvalue()
        mensagem = "Produto comprado com sucesso"
        self.assertTrue(mensagem in saida)

    def test_tela_comprar_produtos_nome_vazio(self):
        self.input.write("\n")
        self.input.seek(0)

        with self.assertRaises(ValueError) as cm:
            self.CLI.tela_comprar_produtos()
        
        mensagem = "O nome do produto não pode ser vazio"
        self.assertTrue(mensagem in cm.exception.args)

    def test_tela_comprar_produtos_produto_inexistente_executa(self):
        self.CLI.business.buy_produto = Mock(return_value=True)
        self.input.writelines([
            "Produto A\n",
            "Marca A\n",
            "Categoria A\n",
            "10.00\n",
            "10"
        ])
        self.input.seek(0)

        self.CLI.tela_comprar_produtos()
        
        saida = self.output.getvalue()
        mensagem = "Produto comprado com sucesso"
        self.assertTrue(mensagem in saida)

    def test_tela_comprar_produtos_cria_produto_corretamente(self):
        produto = Produto("Produto A", 10.00, "Marca A", "Categoria A")
        self.CLI.business.buy_produto = Mock(return_value=True)
        self.input.writelines([
            "Produto A\n",
            "Marca A\n",
            "Categoria A\n",
            "10.00\n",
            "10"
        ])
        self.input.seek(0)

        self.CLI.tela_comprar_produtos()
        
        saida = self.output.getvalue()
        mensagem = str(produto)
        self.assertTrue(mensagem in saida)

    def test_tela_comprar_produtos_produto_inexistente_marca_vazia(self):
        self.input.writelines([
            "Produto A\n",
            "\n",
        ])
        self.input.seek(0)

        with self.assertRaises(ValueError) as cm:
            self.CLI.tela_comprar_produtos()
        
        mensagem = "A marca do produto não pode ser vazia"
        self.assertTrue(mensagem in cm.exception.args)

    def test_tela_comprar_produtos_produto_inexistente_categoria_vazia(self):
        self.input.writelines([
            "Produto A\n",
            "Marca A\n",
            "\n",
        ])
        self.input.seek(0)

        with self.assertRaises(ValueError) as cm:
            self.CLI.tela_comprar_produtos()
        
        mensagem = "A categoria do produto não pode ser vazia"
        self.assertTrue(mensagem in cm.exception.args)

    def test_tela_comprar_produtos_produto_inexistente_preco_vazio(self):
        self.input.writelines([
            "Produto A\n",
            "Marca A\n",
            "Categoria A\n",
            "\n",
        ])
        self.input.seek(0)

        with self.assertRaises(ValueError) as cm:
            self.CLI.tela_comprar_produtos()
        
        mensagem = "O preço do produto não pode ser vazio"
        self.assertTrue(mensagem in cm.exception.args)

    def test_tela_comprar_produtos_quantidade_vazia(self):
        produto = Produto("Produto A", 10.00, "Marca A", "Categoria A")
        self.CLI.business.get_produto_info = Mock(return_value=produto)
        self.input.writelines([
            "Produto A\n",
            "\n",
        ])
        self.input.seek(0)

        with self.assertRaises(ValueError) as cm:
            self.CLI.tela_comprar_produtos()
        
        mensagem = "O número de itens não pode ser vazio"
        self.assertTrue(mensagem in cm.exception.args)

    def test_tela_comprar_produtos_erro(self):
        produto = Produto("Produto A", 10.00, "Marca A", "Categoria A")
        self.CLI.business.get_produto_info = Mock(return_value=produto)
        self.CLI.business.buy_produto = Mock(return_value=False)
        self.input.writelines([
            "Produto A\n",
            "10\n"
        ])
        self.input.seek(0)

        self.CLI.tela_comprar_produtos()
        
        saida = self.output.getvalue()
        mensagem = "[ERRO] Houve um erro ao comprar o produto - operação não realizada"
        self.assertTrue(mensagem in saida)

    def test_tela_vender_produtos_sem_desconto(self):
        produto = Produto("Produto A", 10.00, "Marca A", "Categoria A")
        self.CLI.business.get_produto_info = Mock(return_value=produto)
        self.CLI.business.get_produto_amount = Mock(return_value=10)
        self.CLI.business.sell_produto = Mock(return_value=True)
        self.input.writelines([
            "Produto A\n",
            "\n",
            "7\n"
        ])
        self.input.seek(0)

        self.CLI.tela_vender_produtos()
        
        saida = self.output.getvalue()
        mensagem = "Produto vendido com sucesso"
        self.assertTrue(mensagem in saida)

    def test_tela_vender_produtos_com_desconto(self):
        produto = Produto("Produto A", 10.00, "Marca A", "Categoria A")
        self.CLI.business.get_produto_info = Mock(return_value=produto)
        self.CLI.business.get_produto_amount = Mock(return_value=10)
        self.CLI.business.sell_produto = Mock(return_value=True)
        self.input.writelines([
            "Produto A\n",
            "0.3\n",
            "7\n"
        ])
        self.input.seek(0)

        self.CLI.tela_vender_produtos()
        
        saida = self.output.getvalue()
        mensagem = "Produto vendido com sucesso"
        call_args = self.CLI.business.sell_produto.call_args
        self.assertTrue(mensagem in saida)
        self.assertEqual(call_args.args[2], 0.3)

    def test_tela_vender_produtos_nome_vazio(self):
        self.input.write("\n")
        self.input.seek(0)

        with self.assertRaises(ValueError) as cm:
            self.CLI.tela_vender_produtos()
        
        mensagem = "O nome do produto não pode ser vazio"
        self.assertTrue(mensagem in cm.exception.args)

    def test_tela_vender_produtos_produto_inexistente(self):
        self.input.writelines([
            "Produto A\n",
        ])
        self.input.seek(0)

        self.CLI.tela_vender_produtos()
        
        saida = self.output.getvalue()
        mensagem = "[ERRO] O produto não existe no estoque."
        self.assertTrue(mensagem in saida)

    def test_tela_vender_produtos_quantidade_vazia(self):
        produto = Produto("Produto A", 10.00, "Marca A", "Categoria A")
        self.CLI.business.get_produto_info = Mock(return_value=produto)
        self.CLI.business.get_produto_amount = Mock(return_value=10)
        self.input.writelines([
            "Produto A\n",
            "\n",
            "\n"
        ])
        self.input.seek(0)

        with self.assertRaises(ValueError) as cm:
            self.CLI.tela_vender_produtos()
        
        mensagem = "O número de itens não pode ser vazio"
        self.assertTrue(mensagem in cm.exception.args)

    def test_tela_vender_produtos_erro(self):
        produto = Produto("Produto A", 10.00, "Marca A", "Categoria A")
        self.CLI.business.get_produto_info = Mock(return_value=produto)
        self.CLI.business.get_produto_amount = Mock(return_value=10)
        self.CLI.business.sell_produto = Mock(return_value=False)
        self.input.writelines([
            "Produto A\n",
            "\n",
            "10\n"
        ])
        self.input.seek(0)

        self.CLI.tela_vender_produtos()
        
        saida = self.output.getvalue()
        mensagem = "[ERRO] Houve um erro ao vender o produto - operação não realizada"
        self.assertTrue(mensagem in saida)

    def test_tela_consultar_produto(self):
        self.CLI.handle_criacao_estoque(1)
        
        produto = Produto("Produto A", 10, "Marca A", "Categoria A")
        self.CLI.business.buy_produto(produto, 0)

        self.input.write("Produto A\n")
        self.input.seek(0)

        self.CLI.tela_consultar_produto()

        saida = self.output.getvalue()
        self.assertGreater(saida.find(str(produto)), -1)

    def test_tela_consultar_produto_termina_com_enter(self):
        self.input.write("\n")
        self.input.seek(0)

        sucesso = self.CLI.tela_consultar_produto()

        self.assertTrue(sucesso)

    def test_tela_consultar_produto_inexistente(self):
        self.input.write("Arroz\n")
        self.input.seek(0)

        self.CLI.handle_criacao_estoque(1)
        self.CLI.tela_consultar_produto()


        saida = self.output.getvalue()
        self.assertGreater(saida.find("O produto procurado não existe no catálogo."), -1)

    def test_tela_exibir_catalogo(self):
        produtos = [
            Produto("Produto A", 10.00, "Marca A", "Categoria A"),
            Produto("Produto B", 5.00, "Marca B", "Categoria B")
        ]
        self.CLI.business.listar_estoque = Mock(return_value=produtos)

        self.CLI.tela_exibir_catalogo()

        saida = self.output.getvalue()
        self.assertTrue(str(produtos[0]) in saida)
        self.assertTrue(str(produtos[1]) in saida)

    def test_tela_exibir_catalogo_vazio(self):
        self.CLI.tela_exibir_catalogo()
        saida = self.output.getvalue()
        self.assertGreater(saida.find("O catálogo está vazio"), -1)
    
    def test_tela_ajuda_menu_principal(self):
        self.input.write("\n")
        self.input.seek(0)

        self.CLI.tela_ajuda_menu_principal()

        saida = self.output.getvalue()
        self.assertGreater(saida.find("AJUDA - MENU PRINCIPAL"), -1)

    

