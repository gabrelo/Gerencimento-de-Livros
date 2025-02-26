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

app = Flask(__name__)

livros = [
    {
        'id': 1,
        'titulo': 'O Hobbit',
        'autor': 'J.R.R. Tolkien',
        'ano_publicacao': 1937
    },
    {
        'id': 2,
        'titulo': 'O Senhor dos Anéis',
        'autor': 'J.R.R. Tolkien',
        'ano_publicacao': 1954
    },
    {
        'id': 3,
        'titulo': 'O Silmarillion',
        'autor': 'J.R.R. Tolkien',
        'ano_publicacao': 1977
    },
]

#Consultar (todos) os livros
@app.route('/livros/', methods=['GET'])
def obter_livros():
    return jsonify(livros)


#Consultar um livro pelo id
@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro_por_id(id):
    for livro in livros:
        if livro.get('id') == id:
            return jsonify(livro)
        

#Criar
@app.route('/livros/', methods=['POST'])
def incluir_novo_livro():
    novo_livro = request.get_json()
    livros.append(novo_livro)
    return jsonify(livros)
    

#Editar
@app.route('/livros/<int:id>', methods=['PUT'])
def editar_livro_por_id(id):
    livro_alterado = request.get_json()
    for indice,livro in enumerate(livros):
        if livro.get('id') == id:
            livros[indice].update(livro_alterado)
            return jsonify(livros[indice])
        

#Excluir
@app.route('/livros/<int:id>', methods=['DELETE'])
def excluir_livro_por_id(id):
    for indice,livro in enumerate(livros):
        if livro.get('id') == id:
            livros.pop(indice)
            return jsonify(livros)



if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)

