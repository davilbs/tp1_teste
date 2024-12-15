from estoque import Estoque, EstoqueAlimento
from produto import Produto, ProdutoAlimento
from business import Business

def create_empty_estoque():
    return Estoque()

def create_empty_estoque_alimento():
    return EstoqueAlimento()

def create_produto(nome, preco):
    return Produto(nome, preco)

def create_produto_alimento(nome, preco, validade):
    return ProdutoAlimento(nome, preco, validade)

def create_business(estoque, margin=0.1):
    return Business(estoque, margin)

def main():
    business_type = input('1 - Estoque normal\n2 - Estoque de alimentos\n')
    if business_type == '1':
        business = create_business(create_empty_estoque())
    else:
        business = create_business(create_empty_estoque_alimento())

    option = 0
    while True:
        option = input('1 - Adicionar produto\n2 - Comprar produto\n3 - Vender produto\n4 - Calcular lucro\n5 - Sair\n')
        if option == '1':
            nome = input('Nome do produto: ')
            preco = float(input('Preço do produto: '))
            if business_type == '2':
                validade = input('Data de validade (AAAA-MM-DD): ')
                produto = create_produto_alimento(nome, preco, validade)
            else:
                produto = create_produto(nome, preco)

            if business.buy_produto(produto):
                print('Produto adicionado com sucesso')
            else:
                print('Não foi possível adicionar o produto')
        elif option == '2':
            nome = input('Nome do produto: ')
            amount = int(input('Quantidade: '))
            if business.buy_produto(nome, amount):
                print('Produto comprado com sucesso')
            else:
                print('Não foi possível comprar o produto')
        elif option == '3':
            nome = input('Nome do produto: ')
            amount = int(input('Quantidade: '))
            if business.sell_produto(nome, amount):
                print('Produto vendido com sucesso')
            else:
                print('Não foi possível vender o produto')
        elif option == '4':
            print(f'Lucro total: R$ {business.calculate_profit():.2f}')
        elif option == '5':
            break
        else:
            print('Opção inválida')

if __name__ == '__main__':
    main()