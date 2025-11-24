import os
import csv
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# Definindo a variável de ambiente para modo de desenvolvimento debug
os.environ['FLASK_DEBUG'] = 'True'
app.debug = os.environ.get('FLASK_DEBUG') == 'True'


@app.route('/')
def pagina_home():
    return render_template('index.html')


# Exemplo de rota para a página sobre
@app.route('/sobre')
def pagina_sobre():
    return render_template('sobre.html')


# Exemplo de rota para a página de glossário
@app.route('/glossario')
def glossario():

    glossario_de_termos = []

    with open(
            'bd_glossario.csv',
            newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for l in reader:
            glossario_de_termos.append(l)

    return render_template('glossario.html',
                           glossario=glossario_de_termos)


@app.route('/novo_termo')
def novo_termo():
    return render_template('adicionar_termo.html')


@app.route('/criar_termo', methods=['POST', ])
def criar_termo():
    termo = request.form['termo']
    definicao = request.form['definicao']

    with open(
            'bd_glossario.csv', 'a',
            newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([termo, definicao])

    return redirect(url_for('glossario'))


@app.route('/excluir_termo/<int:termo_id>', methods=['POST'])
def excluir_termo(termo_id):

    with open('bd_glossario.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        linhas = list(reader)

    # Encontrar e excluir o termo com base no ID
    for i, linha in enumerate(linhas):
        if i == termo_id:
            del linhas[i]
            break

    # Salvar as alterações de volta no arquivo
    with open('bd_glossario.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(linhas)

    return redirect(url_for('glossario'))


@app.route('/alterar_termo/<int:termo_id>')
def alterar_termo(termo_id):
    with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        linhas = list(reader)
        termo_para_editar = None
        for i, linha in enumerate(linhas):
            if i == termo_id:
                termo_para_editar = {'id': i, 'termo': linha[0], 'definicao': linha[1]}
                break
    
    if termo_para_editar:
        return render_template('alterar_termo.html', termo=termo_para_editar)
    else:
        return "Termo não encontrado", 404


@app.route('/salvar_termo/<int:termo_id>', methods=['POST'])
def salvar_termo(termo_id):
    termo = request.form['termo']
    definicao = request.form['definicao']

    with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        linhas = list(reader)

    if 0 <= termo_id < len(linhas):
        linhas[termo_id] = [termo, definicao]

    with open('bd_glossario.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(linhas)

    return redirect(url_for('glossario'))


if __name__ == '__main__':
    app.run()
