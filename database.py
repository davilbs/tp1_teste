import sqlite3
from produto import Produto
import os

def create_database():
    if os.path.isfile('database.db'):
        os.remove('database.db')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS businesses
                 (id INTEGER PRIMARY KEY, name TEXT, btype TEXT)''')
    conn.commit()
    conn.close()

# BUSINESS
def add_business(name, btype):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO businesses (name, btype) VALUES (?, ?)', (name, btype))
    create_estoque_table(name, c)
    create_produto_table(name, c)
    create_historico_table(name, c)
    conn.commit()
    conn.close()

# PRODUTO
def create_produto_table(business_name, cur):
    cur.execute(f'''CREATE TABLE IF NOT EXISTS {business_name}_produtos
                 (id INTEGER PRIMARY KEY, nome TEXT, preco REAL, categoria TEXT)''')
    
def get_produto_table(business_name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute(f"SELECT id, nome, preco, categoria FROM {business_name}_produtos")
    except sqlite3.OperationalError:
        create_produto_table(business_name, c)
    finally:
        produtos = c.fetchall()
        conn.close()
    return {produto_id: Produto(nome, preco, None, categoria, produto_id) for produto_id, nome, preco, categoria in produtos}

def add_entry_produto(business_name, nome, preco, categoria):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO {business_name}_produtos (nome, preco, categoria) VALUES (?, ?, ?)", (nome, preco, categoria))
    # Get the id of the new product
    c.execute(f"SELECT id FROM {business_name}_produtos WHERE nome = ?", (nome,))
    produto_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return produto_id

def search_produto(business_name, nome):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f"SELECT id FROM {business_name}_produtos WHERE nome = ?", (nome,))
    produto_id = c.fetchone()
    conn.close()
    return produto_id

def update_produtos(business_name, produto_id, nome=None, preco=None, categoria=None):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Get current attributes
    c.execute(f"SELECT nome, preco, categoria FROM {business_name}_produtos WHERE id = ?", (produto_id,))
    current_nome, current_preco, current_categoria = c.fetchone()
    
    # Update attributes
    nome = nome if nome else current_nome
    preco = preco if preco else current_preco
    categoria = categoria if categoria else current_categoria
    c.execute(f"UPDATE {business_name}_produtos SET nome = ?, preco = ?, categoria = ? WHERE id = ?", (nome, preco, categoria, produto_id))
    conn.commit()
    conn.close()

# ESTOQUE
def create_estoque_table(business_name, cur):
    cur.execute(f'''CREATE TABLE IF NOT EXISTS {business_name}_estoque
                 (id INTEGER PRIMARY KEY, produto_id INTEGER, marca TEXT, quantidade INTEGER, FOREIGN KEY (produto_id) REFERENCES {business_name}_produtos(id))''')
    
def get_estoque_table(business_name, categoria='Sem categoria'):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute(f'''SELECT e.produto_id, e.marca, e.quantidade, p.nome, p.preco, p.categoria
            FROM {business_name}_estoque e
            JOIN {business_name}_produtos p ON e.produto_id = p.id''')
    except sqlite3.OperationalError:
        create_estoque_table(business_name, c)
    finally:
        estoque = c.fetchall()

        conn.close()
    return {produto_id: (Produto(nome, preco, marca, categoria, produto_id), quantidade) for produto_id, marca, quantidade, nome, preco, categoria in estoque}


def add_produto_estoque(business_name, produto_id, marca, quantidade):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO {business_name}_estoque (produto_id, marca, quantidade) VALUES (?, ?, ?)", (produto_id, marca, quantidade))
    # Get the id of the new product
    c.execute(f"SELECT id FROM {business_name}_estoque WHERE produto_id = ?", (produto_id,))
    produto_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return produto_id

def update_estoque(business_name, produto_id, quantidade, marca=None):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Get current marca
    c.execute(f'SELECT marca FROM {business_name}_estoque WHERE produto_id = ?', (produto_id,))
    current_marca = c.fetchone()
    if not current_marca:
        raise ValueError('Produto não cadastrado no estoque')
    
    if marca is not None:
        c.execute(f'UPDATE {business_name}_estoque SET quantidade = ?, marca = ? WHERE produto_id = ?', (quantidade, marca, produto_id))
    else:
        c.execute(f'UPDATE {business_name}_estoque SET quantidade = ? WHERE produto_id = ?', (quantidade, produto_id))
    
    conn.commit()
    conn.close()

def remove_produto_estoque(business_name, produto_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f'DELETE FROM {business_name}_estoque WHERE produto_id = ?', (produto_id,))
    conn.commit()
    conn.close()

# HISTORICO
def create_historico_table(business_name, cur):
    cur.execute(f'''CREATE TABLE IF NOT EXISTS {business_name}_historico
                 (id INTEGER PRIMARY KEY, mensagem TEXT)''')

def get_historico_table(object_name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f'SELECT mensagem FROM {object_name}_historico')
    historico = c.fetchall()
    conn.close()
    return [mensagem for mensagem, in historico]

def add_entry_historico(object_name, mensagem):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f'INSERT INTO {object_name}_historico (mensagem) VALUES (?)', (mensagem,))
    conn.commit()
    conn.close()
