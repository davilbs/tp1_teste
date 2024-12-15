import datetime
import inspect

class Produto:
    nome: str
    preco: float
    marcas: set
    categoria: str

    def __init__(self, nome: str, preco: float, marca: str = None, categoria: str = "Sem categoria"):
        if preco <= 0:
            raise ValueError('Preço deve ser maior que zero')
        self.nome = nome
        self.preco = preco
        self.marcas = set()
        self.categoria = categoria
        self.historico = []
        if marca:
            self.marcas.add(marca)

    def __str__(self):
        marcas_str = ', '.join(self.marcas) if self.marcas else "Nenhuma marca"
        return f'{self.nome} - R$ {self.preco:.2f} - Categoria: {self.categoria} - Marcas: {marcas_str}'
    
    def __repr__(self):
        return f'Produto(nome={self.nome}, preco={self.preco:.2f}, categoria={self.categoria}, marcas={self.marcas})'
    
    def registrar_historico(self, mensagem: str):
        metodo_chamador = inspect.stack()[1].function
        data_hora = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.historico.append(f"{data_hora} - Método: [{metodo_chamador}] - Ação: {mensagem}")
    
    def alterar_categoria(self, nova_categoria: str):
        if not nova_categoria:
            raise ValueError('A categoria não pode ser vazia')
        self.categoria = nova_categoria
        self.registrar_historico(f'Categoria alterada para "{nova_categoria}"')
    
    def aplicar_desconto(self, percentual: float):
        if percentual < 0 or percentual > 100:
            raise ValueError('O desconto deve estar entre 0% e 100%')
        desconto = self.preco * (percentual / 100)
        self.preco -= desconto
        self.registrar_historico(f'Desconto de {percentual}% aplicado. Preço final: R$ {self.preco:.2f}')

    # Método para restaurar o preço original (se armazenarmos o preço base)
    def restaurar_preco(self, preco_original: float):
        if preco_original <= 0:
            raise ValueError('O preço original deve ser maior que zero')
        self.preco = preco_original
        self.registrar_historico(f'Preço restaurado para R$ {preco_original:.2f}')

    def add_marca(self, marca: str):
        self.marcas.add(marca)
        self.registrar_historico(f'Marca {marca} adicionada ao produto')

    def remove_marca(self, marca: str):
        if marca in self.marcas:
            self.marcas.remove(marca)
            self.registrar_historico(f'Marca {marca} removida do produto')
        else:
            raise KeyError(f'Marca {marca} nã0 encontrada no produto')


class ProdutoAlimento(Produto):
    validade: datetime.date
    def __init__(self, nome, preco, validade: str = None, vegano: bool = False, marca=None, categoria: str = "Sem categoria"):
        super().__init__(nome, preco, marca, categoria)
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