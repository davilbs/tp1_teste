from produto import Produto, ProdutoAlimento
from typing import Dict
import datetime

class Estoque:
    def __init__(self):
        self._estoque = {}
        self._produtos = {}

    def buy_produto(self, produto: Produto | str, amount=1):
        if isinstance(produto, Produto):
            if produto not in self._estoque:
                self._estoque[produto.nome] = 0
            self._estoque[produto.nome] += amount
        else:
            if self.get_produto_info(produto) is None:
                return False
            self._estoque[produto] += amount
        return True

    def sell_produto(self, produto, amount=1):
        if produto not in self._estoque:
            return False
        if self._estoque[produto] <= amount:
            return False
        self._estoque[produto] -= amount
        return True
    
    def add_produto(self, produto: Produto):
        if produto.nome not in self._produtos:
            self._produtos[produto.nome] = produto
            self._estoque[produto.nome] = 0
            return True
        return False
    
    def remove_produto(self, produto: Produto):
        if produto.nome in self._produtos:
            del self._produtos[produto.nome]
            return True
        return False
    
    def get_produto_amount(self, produto) -> int:
        return self._estoque.get(produto, 0)
    
    def get_produto_info(self, nome) -> Produto | None:
        return self._produtos.get(nome, None)

    def get_estoque_size(self) -> int:
        total = 0
        for produto in self._produtos:
            total += self._estoque[produto]
        return total
    
    def get_estoque(self) -> list[Produto]:
        lista_produtos = []
        for produto in self._produtos:
            lista_produtos.append(self._produtos[produto])
        return lista_produtos
    
class EstoqueAlimento(Estoque):
    _produtos: Dict[str, ProdutoAlimento]

    def __init__(self):
        super().__init__()
        self._produtos = {}

    def add_produto(self, produto: ProdutoAlimento):
        if produto.nome not in self._produtos:
            self._produtos[produto.nome] = produto
        return True
    
    def get_produto_info(self, nome):
        return self._produtos.get(nome, None)
    
    def remove_vencidos(self, data: str):
        curr_produtos = list(self._produtos.values())
        for produto in curr_produtos:
            if produto.validade and produto.validade < datetime.datetime.strptime(data, '%Y-%m-%d').date():
                del self._produtos[produto.nome]
        return True