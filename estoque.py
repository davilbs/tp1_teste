from produto import Produto, ProdutoAlimento
from typing import Dict
import datetime

class Estoque:
    def __init__(self):
        self._estoque = {}
        self._produtos = {}

    def buy_produto(self, produto, amount=1):
        if produto not in self._estoque:
            self._estoque[produto] = 0
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
            return True
        return False
    
    def remove_produto(self, produto: Produto):
        if produto.nome in self._produtos:
            del self._produtos[produto.nome]
            return True
        return False
    
    def get_produto_amount(self, produto):
        return self._estoque.get(produto, 0)
    
    def get_produto_info(self, nome):
        return self._produtos.get(nome, None)

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