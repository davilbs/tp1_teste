from estoque import Estoque
from produto import Produto

class Business():
    def __init__(self, estoque: Estoque, margin=0.1):
        self._estoque = estoque
        self._transactions = []
        self._margin = margin

    def calculate_profit(self):
        profit = 0
        for transaction in self._transactions:
            profit += transaction[0] * transaction[1]
        return profit
    
    def get_estoque_size(self):
        return self._estoque.get_estoque_size()
    
    def get_produto_info(self, nome):
        return self._estoque.get_produto_info(nome)
    
    def calculate_buy_price(self, preco):
        # O preço de compra é o preço de venda + a margem
        return -(preco * (1 - self._margin))
    
    def compute_transaction(self, nome, amount, ttype='buy'):
        produto = self.get_produto_info(nome)
        if produto is None:
            return False
        
        if ttype == 'sell':
            self._transactions.append((produto.preco, amount))
        else:
            buy_price = self.calculate_buy_price(produto.preco)
            self._transactions.append((buy_price, amount))

        return True
    
    def buy_produto(self, produto: str, amount=1):
        self._estoque.buy_produto(produto, amount)
        return self.compute_transaction(produto, amount)

    def buy_produto(self, produto: Produto, amount=1):
        self._estoque.add_produto(produto)
        self.buy_produto(produto.nome, amount)
        return self.compute_transaction(produto.nome, amount)

        
    
    def sell_produto(self, nome, amount):
        self.compute_transaction(nome, amount, 'sell')
        return self._estoque.sell_produto(nome, amount)