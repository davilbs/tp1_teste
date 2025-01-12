from estoque import Estoque
from produto import Produto
from typing import Literal
from database import search_produto, add_entry_historico
class Business():
    def __init__(self, nome: str, estoque: Estoque, margin: float = 0.1):
        self.nome = nome
        self._estoque = estoque if estoque != None else Estoque()
        self._transactions = []
        self._margin = margin
        self.desconto = 0

    def registrar_historico(self, mensagem: str):
        add_entry_historico(self.nome, mensagem)

    def calculate_profit(self) -> float:
        profit = 0
        for transaction in self._transactions:
            profit += transaction[0] * transaction[1]
        self.registrar_historico(f'Lucro total: R$ {profit:.2f}')
        return profit

    def alterar_nome(self, novo_nome: str):
        if not novo_nome:
            raise ValueError('O nome não pode ser vazio')
        self.nome = novo_nome
        self.registrar_historico(f'Nome alterado para "{novo_nome}"')

    def set_desconto(self, percentual: float):
        if percentual < 0 or percentual > 100:
            raise ValueError('O desconto deve estar entre 0% e 100%')
        self.desconto = percentual
        self.registrar_historico(f'Promoção de {percentual}%')

    def get_estoque_size(self) -> int:
        return self._estoque.get_estoque_size()
    
    def get_produto_info(self, nome: str) -> Produto | None:
        id = search_produto(self.nome, nome)
        return self._estoque.get_produto_info(id)
    
    def listar_estoque(self) -> list[str]:
        return [str(produto) for produto in self._estoque.get_estoque()]
    
    def calculate_buy_price(self, preco) -> float:
        # O preço de compra é o preço de venda + a margem
        return -(preco * (1 - self._margin))
    
    def compute_transaction(self, produto_id: int, amount: int, ttype: Literal['buy', 'sell']='buy', desconto: float = 0):
        produto = self.get_produto_info(produto_id)
        if produto is None:
            return False
        
        if ttype == 'sell':
            produto.aplicar_desconto(desconto)
            self._transactions.append((produto.preco, amount))
            produto.restaurar_preco(produto.preco)
            self.registrar_historico(f'Venda de {amount} unidades de {produto_id}')
        else:
            buy_price = self.calculate_buy_price(produto.preco)
            self._transactions.append((buy_price, amount))
            self.registrar_historico(f'Compra de {amount} unidades de {produto_id}')

        return True

    def buy_produto(self, produto: Produto | str, amount: int = 0):
        if isinstance(produto, Produto):
            produto = self._estoque.add_produto(produto)
            try:
                self._estoque.buy_produto(produto, amount)
                self.compute_transaction(produto.id, amount)
                return True
            except ValueError:
                return False
        else:
            if self._estoque.buy_produto(produto, amount):
                return self.compute_transaction(produto, amount)
        return False

    def get_produto_amount(self, nome: str) -> int:
        return self._estoque.get_produto_amount(nome)
    
    def sell_produto(self, produto_id: str, amount: int, desconto: float = 0):
        if self._estoque.sell_produto(produto_id, amount):
            return self.compute_transaction(produto_id, amount, 'sell', desconto)
        return False
    
    def remove_produto(self, nome: str):
        return False # Esqueleto temporário