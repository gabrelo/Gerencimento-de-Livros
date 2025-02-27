#API - É um lugar para disponibilizar recursos e/ou funcionalidades
#1 - Objetivo - Criar uma api para disponibilizar a consulta, criação, edição e exclusão de livros.
#2 - URL base - localhost.com
#3 - Endpoints - 
#   3.1 - /livros - GET - Consultar todos os livros
#   3.2 - /livros - POST - Cadastrar um livro
#   3.3 - /livros/{id} - GET - Consultar um livro pelo id
#   3.4 - /livros/{id} - PUT - Atualizar um livro pelo id
#   3.5 - /livros/{id} - DELETE - Excluir um livro pelo id
#4 - Quais recursos - Livros

from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

#Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('livros.db')
    conn.row_factory = sqlite3.Row #Permite acessar colunas pelo nome
    return conn

#Criar a tabela se ela não existir
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano_publicacao INTEGER
    )''')
    # Inserir dados iniciais apenas se a tabela estiver vazia
    conn.execute('INSERT OR IGNORE INTO livros (id, titulo, autor, ano_publicacao) VALUES (1, "O Hobbit", "J.R.R. Tolkien", 1937)')
    conn.execute('INSERT OR IGNORE INTO livros (id, titulo, autor, ano_publicacao) VALUES (2, "O Senhor dos Anéis", "J.R.R. Tolkien", 1954)')
    conn.execute('INSERT OR IGNORE INTO livros (id, titulo, autor, ano_publicacao) VALUES (3, "O Silmarillion", "J.R.R. Tolkien", 1977)')
    conn.commit()
    conn.close()


#Consultar (todos) os livros
@app.route('/livros/', methods=['GET'])
def obter_livros():
    conn = get_db_connection()
    livros = conn.execute('SELECT * FROM livros').fetchall()
    conn.close()
    return jsonify([dict(livro) for livro in livros])


#Consultar um livro pelo id
@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro_por_id(id):
    conn = get_db_connection()
    livro = conn.execute('SELECT * FROM livros WHERE id = ?', (id,)).fetchone()
    conn.close()
    
        

#Criar
@app.route('/livros/', methods=['POST'])
def incluir_novo_livro():
    novo_livro = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO livros (titulo, autor, ano_publicacao) VALUES (?, ?, ?)', (novo_livro['titulo'], novo_livro['autor'], novo_livro['ano_publicacao']))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': novo_id, **novo_livro}), 201
    

#Editar
@app.route('/livros/<int:id>', methods=['PUT'])
def editar_livro_por_id(id):
    livro_alterado = request.get_json()
    conn = get_db_connection()
    conn.execute(
        'UPDATE livros SET titulo = ?, autor = ?, ano_publicacao = ? WHERE id = ?',
        (livro_alterado['titulo'], livro_alterado['autor'], livro_alterado['ano_publicacao'], id)
    )
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Livro atualizado'})
        

#Excluir
@app.route('/livros/<int:id>', methods=['DELETE'])
def excluir_livro_por_id(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM livros WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Livro excluído'})



if __name__ == '__main__':
    init_db() #Inicializa o banco de dados
    app.run(port=5000, host='localhost', debug=True)

#Fim do código

