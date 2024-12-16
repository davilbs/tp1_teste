from sys import stdin, stdout
from estoque import Estoque, EstoqueAlimento
from produto import Produto, ProdutoAlimento
import os
from business import Business

class CLI:
    def __init__(self, infile=stdin, outfile=stdout) -> None:
        self.infile = infile
        self.outfile = outfile
        self._atty = self.infile.isatty()
        self.business = Business("")

        if not self._atty:
            pos = self.infile.tell()
            self.infile.seek(os.SEEK_END)
            self._final_pos = self.infile.tell()
            self._final_pos = self.infile.tell()
            self.infile.seek(pos)
    
    def print(self, *values: object, sep: str | None =" ", end: str | None = "\n", flush: bool = False) -> None:
        print(*values, sep=sep, end=end, file=self.outfile, flush=flush)
    
    def print_opcao_invalida(self) -> None:
        self.print("Opção inválida. Por favor, escolha uma das opções disponíveis.")
    
    def input(self, prompt: object = "> ") -> str | None:
        self.print(prompt, sep='', end='', flush=True)

        if not self._atty:
            if self.infile.tell() == self._final_pos:
                raise EOFError
        
        return self.infile.readline()[:-1]

    def start(self):
        try:
            self.print("Seja bem vindo ao sistema de gestão de estoques. Pressione Ctrl+C a qualquer\n"
                       "momento para encerrar o programa.\n")
            tipo_estoque = self.tela_escolher_tipo_estoque()
            # Se o tipo_estoque é None, é porque ele teve um EOFError - chegou ao fim da entrada sem ler um valor válido.
            if tipo_estoque is None:
                self.print("\nEncerrando...")
                return
            
            self.handle_criacao_estoque(tipo_estoque)
            self.tela_info_funcionamento()

            while True:
                opcao = self.tela_menu_principal()
                match opcao:
                    case 1:
                        try:
                            self.tela_adicionar_produtos()
                        except ValueError as ex:
                            self.print("[ERRO]", *ex.args)
                    case 2:
                        self.tela_remover_produtos()
                    case 3:
                        try:
                            self.tela_comprar_produtos()
                        except ValueError as ex:
                            self.print("[ERRO]", *ex.args)    
                    case 5:
                        sucesso = self.tela_consultar_produto()
                        if not sucesso:
                            self.print("\nEncerrando...")
                            return
                    case 6:
                        self.tela_exibir_catalogo()
                    case 7:
                        self.tela_ajuda_menu_principal()
                        continue
        except KeyboardInterrupt:
            self.print("\nEncerrando...")
            return
        except EOFError:
            self.print("\nEncerrando...")
            return
        except Exception as ex:
            self.print("[ERRO] Um erro ocorreu durante a execução do programa:",
                       *ex.args)
            self.print("\nEncerrando...")
            return
            

    def tela_escolher_tipo_estoque(self) -> int | None:
        tipo = None

        try:
            while True:
                self.print("\n[TIPO DE ESTOQUE]")
                self.print("Escolha o seu tipo de estoque:")
                self.print("1) Estoque genérico: armazena produtos de forma genérica.")
                self.print("2) Estoque de alimentos: possui funcionalidades específicas para alimentos,\n"
                        "   como remover todos os produtos vencidos.")
                
                string = self.input().strip()
                match string:
                    case "1":
                        tipo = 1
                        self.print("Tipo escolhido: Estoque Genérico")
                        break
                    case "2":
                        tipo = 2
                        self.print("Tipo escolhido: Estoque de alimentos")
                        break
                    case _:
                        self.print_opcao_invalida()
                        continue
        except EOFError:
            return None
        
        return tipo
    
    def handle_criacao_estoque(self, tipo_estoque: int) -> None:
        match tipo_estoque:
            case 1:
                self.estoque = Estoque()
                self.is_estoque_alimento = False
            case 2:
                self.estoque = EstoqueAlimento()
                self.is_estoque_alimento = True
            case _:
                raise Exception("O tipo de estoque recebido não é um tipo válido.")
        self.business.set_estoque(self.estoque)

    def tela_info_funcionamento(self) -> None:
        self.print("\n[FUNCIONAMENTO DO SISTEMA]")
        self.print("O estoque mantém um catálogo de produtos, assim como uma relação das")
        self.print("quantidades. Para comprar um produto para o estoque ou vender um produto para um")
        self.print("cliente, é preciso que o produto tenha sido adicionado ao catálogo primeiro.")
        self.input("Pressione ENTER para prosseguir...")
    
    def tela_menu_principal(self) -> int:
        opcao = None

        while True:
            self.print("\n[MENU PRINCIPAL]")
            self.print("1) Adicionar produtos ao catálogo")
            self.print("2) Remover produtos do catálogo")
            self.print("3) Comprar produtos")
            self.print("4) Vender produtos")
            self.print("5) Consultar produtos")
            self.print("6) Catálogo")
            self.print("7) Ajuda")


            opcao = self.input().strip()
            match opcao:
                case "1" | "2" | "3" | "4" | "5" | "6" | "7":
                    opcao = int(opcao)
                    break
                case _:
                    self.print_opcao_invalida()
                    continue
        
        return opcao
    
    def tela_ajuda_menu_principal(self):
        self.print("\n[AJUDA - MENU PRINCIPAL]")
        self.print(
            "1) Adicionar produtos ao catálogo: Adiciona um novo produto ao catálogo do\n"
            "   estoque, para que unidades dele possam ser compradas e vendidas.\n"
            "2) Remover produtos do catálogo: Remove um produto do catálogo do estoque. Requer\n"
            "   que não existam unidades do produto em estoque antes que ele possa ser\n"
            "   removido.\n"
            "3) Comprar produtos: Compra unidades de um produto em catálogo para o estoque.\n"
            "   Requer que o produto desejado exista no catálogo.\n"
            "4) Vender produtos: Vende unidades de um produto em estoque. O produto precisa\n"
            "   existir no catálogo, e o estoque precisa ter unidades o suficiente.\n"
            "5) Consultar produtos: Mostra as informações do produto armazenadas no catálogo e\n"
            "   no estoque.\n"
            "6) Catálogo: Exibe todos os produtos do estoque.\n"
            "7) Ajuda: Exibe este painel de ajuda."
        )
        self.input("Pressione ENTER para prosseguir...")
        return 

    def tela_adicionar_produtos(self):
        self.print("\n[ADICIONAR PRODUTOS AO CATÁLOGO - MENU PRINCIPAL]")
        self.print("Escreva o nome do produto:\n")
        nome = self.input()
        if nome == "":
            raise ValueError ("O nome do produto não pode ser vazio")
        self.print("Escreva a marca do produto")
        marca = self.input()
        if marca == "":
            raise ValueError ("A marca do produto não pode ser vazia")
        self.print("Escreva a categoria do produto:\n")
        categoria = self.input()
        if categoria == "":
            raise ValueError ("A categoria do produto não pode ser vazia")
        self.print("Aplique o preço do produto:\n")
        preco = float(self.input())
        if preco == "":
            raise ValueError ("O preço do produto não pode ser vazio")
        self.print("Escreva o desconto do produto:\n")
        desconto = self.input()
        produto = Produto(nome, preco, marca, categoria)
        if desconto != "":
            produto.aplicar_desconto(float(desconto))
        print("Produto adicionado com sucesso!")
        self.print(produto)
        self.business.buy_produto(produto)

    def tela_remover_produtos(self):
        self.print("\n[REMOVER PRODUTOS DO CATÁLOGO - MENU PRINCIPAL]")

    def tela_comprar_produtos(self):
        self.print("\n[COMPRAR PRODUTOS - MENU PRINCIPAL]")
        self.print("Escreva o nome do produto:\n")
        nome = self.input()
        if nome == "":
            raise ValueError ("O nome do produto não pode ser vazio")
        self.print("Escreva a marca do produto")
        marca = self.input()
        if marca == "":
            raise ValueError ("A marca do produto não pode ser vazia")
        self.print("Escreva a categoria do produto:\n")
        categoria = self.input()
        if categoria == "":
            raise ValueError ("A categoria do produto não pode ser vazia")
        self.print("Aplique o preço do produto:\n")
        preco = float(self.input())
        if preco == "":
            raise ValueError ("O preço do produto não pode ser vazio")
        self.print("Escreva o desconto do produto:\n")
        desconto = self.input()
        produto = Produto(nome, preco, marca, categoria)
        if desconto != "":
            produto.aplicar_desconto(float(desconto))
        print("Produto comprado com sucesso!")
        self.print(produto)

    def tela_vender_produtos(self):
        self.print("\n[REMOVER PRODUTOS DO CATÁLOGO - MENU PRINCIPAL]")

    def tela_exibir_catalogo(self):
        lista_produtos = self.business.listar_estoque()

        if len(lista_produtos) == 0:
            self.print("O catálogo está vazio.")
            return
        
        self.print("[CATÁLOGO]")
        self.print(*[f"- {prod}" for prod in self.business.listar_estoque()], sep="\n")

    def tela_consultar_produto(self) -> bool:
        try:
            while True:
                self.print("\n[CONSULTAR PRODUTO]")
                self.print("Digite o nome do produto que deseja consultar, ou pressione ENTER para voltar:")
                nome = self.input()
                match nome:
                    case "":
                        break
                    case _:
                        produto = self.business.get_produto_info(nome)
                        if produto is None:
                            self.print("O produto procurado não existe no catálogo.", flush=True)
                            continue

                        self.print(str(produto))
                        qtd = self.business.get_produto_amount(nome)
                        self.print(f"Quantidade em estoque: {qtd}")
            return True
        except EOFError:
            return False
                    


