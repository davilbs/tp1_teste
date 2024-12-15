from sys import stdin, stdout
from estoque import Estoque, EstoqueAlimento
from produto import Produto, ProdutoAlimento

class CLI:
    def __init__(self, infile=stdin, outfile=stdout) -> None:
        self.infile = infile
        self.outfile = outfile
    
    def print(self, *values: object, sep: str | None =" ", end: str | None = "\n", flush: bool = False) -> None:
        print(*values, sep=sep, end=end, file=self.outfile, flush=flush)
    
    def print_opcao_invalida(self) -> None:
        self.print("Opção inválida. Por favor, escolha uma das opções disponíveis.")
    
    def input(self, prompt: object = "> ") -> str:
        self.print(prompt, sep='', end='', flush=True)
        return self.infile.readline()

    def start(self):
        try:
            self.print("Seja bem vindo ao sistema de gestão de estoques. Pressione Ctrl+C a qualquer\n"
                       "momento para encerrar o programa.\n")
            tipo_estoque = self.tela_escolher_tipo_estoque()
            self.handle_criacao_estoque(tipo_estoque)
            self.tela_info_funcionamento()

            while True:
                opcao = self.tela_menu_principal()
                match opcao:
                    case 6:
                        self.tela_ajuda_menu_principal()
        except KeyboardInterrupt:
            self.print("\nEncerrando...")
            return
        except Exception as ex:
            self.print("[ERRO] Um erro ocorreu durante a execução do programa:",
                       *ex.args)
            self.print("\nEncerrando...")
            return
            

    def tela_escolher_tipo_estoque(self) -> int:
        tipo = None

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
            self.print("6) Ajuda")

            opcao = self.input().strip()
            match opcao:
                case "1" | "2" | "3" | "4" | "5" | "6":
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
            "6) Ajuda: exibe este painel de ajuda."
        )
        self.input("Pressione ENTER para prosseguir...")
    
    # def tela_consultar_produto(self):
    #     while True:
    #         self.print("\n[CONSULTAR PRODUTO]")
    #         self.print("Digite o nome do produto que deseja consultar, :")
    #         nome = self.input()
    #         self.estoque.get_produto_info(nome)

