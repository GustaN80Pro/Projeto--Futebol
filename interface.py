from googlesearch import search
import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('jogadores.db')
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jogadores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        imagem_url TEXT
    )
''')
conn.commit()

def cadastrar_jogador(nome):
    # Verificar se o jogador já está no banco de dados
    cursor.execute('SELECT * FROM jogadores WHERE nome = ?', (nome,))
    jogador = cursor.fetchone()

    if jogador:
        print(f'O jogador {nome} já está cadastrado.')
    else:
        # Fazer uma busca no Google pelo nome do jogador
        query = f'{nome} jogador'
        for j in search(query, num=1, stop=1):
            imagem_url = j
            break

        # Adicionar o jogador ao banco de dados
        cursor.execute('INSERT INTO jogadores (nome, imagem_url) VALUES (?, ?)', (nome, imagem_url))
        conn.commit()
        print(f'O jogador {nome} foi cadastrado com sucesso.')

def obter_imagem_url(nome):
    # Buscar a imagem do jogador no banco de dados
    cursor.execute('SELECT imagem_url FROM jogadores WHERE nome = ?', (nome,))
    imagem_url = cursor.fetchone()

    if imagem_url:
        print(f'Link da imagem do jogador {nome}: {imagem_url[0]}')
    else:
        print(f'Jogador {nome} não encontrado.')

# Exemplo de uso
cadastrar_jogador('Messi')
obter_imagem_url('Messi')

# Fechar a conexão com o banco de dados
conn.close()