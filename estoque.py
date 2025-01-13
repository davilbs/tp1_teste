from produto import Produto, ProdutoAlimento
from typing import Dict
import datetime
from database import search_produto, get_estoque_table, get_produto_table, add_produto_estoque, update_estoque, add_entry_produto

class Estoque:
    def __init__(self, business_name):
        business_name = business_name.replace(' ', '_')
        self._business = business_name
        self._estoque = get_estoque_table(business_name)
        self._produtos = get_produto_table(business_name)

    def buy_produto(self, produto: Produto | str, amount=1):
        id_produto = produto
        if isinstance(produto, Produto):
            id_produto = produto.id
            
        if self.get_produto_info(str(id_produto)) == None:
            raise ValueError('Produto não cadastrado no estoque')
        
        update_estoque(self._business, id_produto, self._estoque.get(int(id_produto))[1] + amount)
        self._estoque = get_estoque_table(self._business)
        return True

    def sell_produto(self, produto_id: str, amount=1):
        if self._estoque.get(int(produto_id)) is None:
            return False
        
        if self._estoque.get(int(produto_id))[1] <= amount:
            return False
        
        update_estoque(self._business, produto_id, self._estoque.get(int(produto_id))[1] - amount)
        self._estoque = get_estoque_table(self._business)
        return True
    
    def add_produto(self, produto: Produto):
        if (produto.id is None) or (produto.id not in self._produtos):
            new_id = add_entry_produto(self._business, produto.nome, produto.preco, produto.categoria)
            add_produto_estoque(self._business, new_id, produto.marca, 0)
            self._produtos = get_produto_table(self._business)
            self._estoque = get_estoque_table(self._business)
        return Produto(nome=produto.nome, preco=produto.preco, categoria=produto.categoria, id=new_id)
            
    def remove_produto(self, produto: Produto):
        if self._produtos.get(produto.id):
            del self._produtos[produto.id]
            return True
        return False
    
    def get_produto_amount(self, produto_id: str) -> int:
        if not produto_id.isnumeric():
            produto_id = self.get_produto_info(produto_id).id
        return self._estoque.get(produto_id, 0)[1]
    
    def get_produto_info(self, produto: str) -> Produto | None:
        if not produto.isnumeric():
            ids = search_produto(self._business, produto)
            if not ids:
                return None
            produto = self._produtos.get(int(ids[0]))
        else:
            produto = self._produtos.get(int(produto))
        return produto

    def get_estoque_size(self) -> int:
        total = 0
        for produto in self._produtos.keys():
            total += self._estoque.get(int(produto))[1]
        return total
    
    def get_estoque(self) -> list[Produto]:
        lista_produtos = []
        for produto in self._produtos:
            lista_produtos.append(self._produtos[produto])
        return lista_produtos
    
class EstoqueAlimento(Estoque):
    _produtos: Dict[str, ProdutoAlimento]

    def __init__(self, business_nome):
        super().__init__(business_nome)

    def add_produto(self, produto: ProdutoAlimento):
        if (produto.id is None) or (produto.id not in self._produtos):
            new_id = add_entry_produto(self._business, produto.nome, produto.preco, produto.categoria)
            add_produto_estoque(self._business, new_id, produto.marca, 0)
            if produto.validade:
                new_produto = ProdutoAlimento(nome=produto.nome, preco=produto.preco, categoria=produto.categoria, validade=produto.validade.isoformat(), id=new_id)
            else:
                new_produto = ProdutoAlimento(nome=produto.nome, preco=produto.preco, categoria=produto.categoria, id=new_id)
            self._produtos[new_id] = new_produto
            self._estoque = get_estoque_table(self._business)
        return new_produto