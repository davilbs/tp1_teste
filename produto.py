import datetime
import inspect

class Produto:
    id: int
    nome: str
    preco: float
    marca: set
    categoria: str

    def __init__(self, nome: str, preco: float, marca: str = None, categoria: str = "Sem categoria", id: int = None):
        if preco <= 0:
            raise ValueError('Preço deve ser maior que zero')
        self.id = id
        self.nome = nome
        self.preco = preco
        self.marca = "Nenhuma marca"
        self.categoria = categoria
        self.historico = []
        if marca:
            self.marca = marca

    def __str__(self):
        return f'{"" if self.id is None else f"ID {self.id} - "}Nome: {self.nome} - Preço: R$ {self.preco:.2f} - Categoria: {self.categoria} - Marcas: {self.marca}'
    
    def __repr__(self):
        return f'Produto(id={self.id}, nome={self.nome}, preco={self.preco:.2f}, categoria={self.categoria}, marcas={self.marca})'
    
    def registrar_historico(self, mensagem: str):
        self.historico.append(mensagem)
    
    def alterar_categoria(self, nova_categoria: str):
        if not nova_categoria:
            raise ValueError('A categoria não pode ser vazia')
        self.categoria = nova_categoria
        self.registrar_historico(f'Categoria alterada para "{nova_categoria}"')
    
    def aplicar_desconto(self, desconto: float):
        if desconto < 0 or desconto > 1:
            raise ValueError('O desconto deve estar entre 0% e 100%')
        val_desconto = self.preco * desconto
        self.preco -= val_desconto
        self.registrar_historico(f'Desconto de {round(desconto * 100)}% aplicado. Preço final: R$ {self.preco:.2f}')

    # Método para restaurar o preço original (se armazenarmos o preço base)
    def restaurar_preco(self, preco_original: float):
        if preco_original <= 0:
            raise ValueError('O preço original deve ser maior que zero')
        self.preco = preco_original
        self.registrar_historico(f'Preço restaurado para R$ {preco_original:.2f}')

    def set_marca(self, marca: str):
        self.marca = marca
        self.registrar_historico(f'Marca {marca} definida para o produto')

    def remove_marca(self):
        self.registrar_historico(f'Marca {self.marca} removida do produto')
        self.marca = "Nenhuma marca"


class ProdutoAlimento(Produto):
    validade: datetime.date
    def __init__(self, nome, preco, validade: str = None, vegano: bool = False, marca=None, categoria: str = "Alimento", id: int = None):
        super().__init__(nome, preco, marca, categoria, id)
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
        validade = datetime.datetime.strptime(validade, '%Y-%m-%d').date()
        self.validade = validade