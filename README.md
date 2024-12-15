# Trabalho Prático 1 - Teste de Software
Repositório para trabalho prático de Teste de Software - DCC - UFMG

### Grupo:
* Davi Lage Borges Souza 
* Gabriel Coelho
* Thiago Amorim

## Sistema
Este sistema é um gerenciador de estoque de produtos, desenvolvido como parte do trabalho prático de Teste de Software do curso de DCC na UFMG. Ele permite o cadastro, atualização, remoção e consulta de produtos no estoque. O sistema é composto pelos seguintes módulos:

- `produto.py`: Define a classe [`Produto`](produto.py), que representa um produto no estoque, com atributos como nome, preço e quantidade. Também define a classe [`ProdutoAlimento`](produto.py), que herda de `Produto` e adiciona atributos específicos para alimentos, como validade e se é vegano.
- `estoque.py`: Define a classe [`Estoque`](estoque.py), que gerencia uma coleção de produtos, permitindo operações de adicionar, remover e atualizar produtos no estoque. Também define a classe [`EstoqueAlimento`](estoque.py), que herda de `Estoque` e adiciona funcionalidades específicas para alimentos, como a remoção de produtos vencidos.
- `business.py`: Define a classe [`Business`](business.py), que gerencia as transações de compra e venda de produtos, calculando o lucro e mantendo o controle do estoque.
- `main.py`: Contém a função [`main`](main.py) que inicializa o sistema e permite a interação com o usuário através de um menu de opções.

O sistema também inclui testes automatizados para garantir a qualidade e a correção das funcionalidades implementadas. Os testes estão localizados nos arquivos [`test_estoque.py`](test_estoque.py), [`test_estoque_alimento.py`](test_estoque_alimento.py), [`test_produto.py`](test_produto.py) e [`test_produto_alimento.py`](test_produto_alimento.py).

## Tecnologias utilizadas
- Python 3
- Poetry para gerenciamento de dependências
- Unittest para testes automatizados


## Instalação
1. Criar ambiente virtual python
`python3 -m venv .venv/tp1`

2. Entrar no ambiente virtual
`source .venv/tp1/bin/activate`

3. Instalar o poetry
`python3 -m pip install -r requirements.txt`

4. Inicializar o módulo
`poetry install`