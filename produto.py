import datetime
class Produto:
    nome: str
    preco: float
    marca: set

    def __init__(self, nome: str, preco: float, marca: str = None):
        if preco <= 0:
            raise ValueError('Preço deve ser maior que zero')
        self.nome = nome
        self.preco = preco
        self.marcas = set()
        if marca:
            self.marcas.add(marca)

    def __str__(self):
        return f'{self.nome} - R$ {self.preco:.2f}'
    
    def __repr__(self):
        return f'Produto({self.nome}, {self.preco})'
    
    def add_marca(self, marca):
        self.marcas.add(marca)

    def remove_marca(self, marca):
        self.marcas.remove(marca)

class ProdutoAlimento(Produto):
    validade: datetime.date
    def __init__(self, nome, preco, validade: str = None, vegano: bool = False, marca=None):
        super().__init__(nome, preco, marca)
        self.vegano = vegano
        if validade:
            self.set_validade(validade)
        else:
            self.validade = None

    def __str__(self):
        return f'{self.nome} - R$ {self.preco:.2f}{" vegano" if self.vegano else ""}{f" - {self.validade.isoformat()}" if self.validade else ""}'

    def __repr__(self):
        return f'ProdutoAlimento({self.nome}, {self.preco}, {self.vegano}, {self.validade})'
    
    def set_vegano(self, vegano):
        self.vegano = vegano
    
    def set_validade(self, validade: str):
        self.validade = datetime.datetime.strptime(validade, '%Y-%m-%d').date()