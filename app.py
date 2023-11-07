from flask import Flask, render_template, request, redirect, session
# importando flask e todas as classes que vamos usar 
# chama o html(extend), redenriza pagina html (render_template)
# pega respostas e dados de um formulario (request)
# rota, função, apontando para uma rota que ja existe (redirect)
# chama sessao (session)
import sqlite3 as sql
import uuid
# serve para gerar nomes/numeros aleatorios unicos para as imagens, gera numeros aleatorios para concatenar com os nomes das imagens que serao utilizadas (uuid)
app = Flask(__name__)
app.secrect_key = "quitandazezinho"
# salvar sessao e colocar ums especie de segruança (secrect_key)
usuario = 'Seu José'
senha = 'Eu,Zé'
login = 'False'
# FUNÇÃO PARA VERIFICAR SESSÃO ↧
def verifica_sessao():
    if 'login' in session and session['login']:
        return True
    else:
        return False
# CONEXÃO COM O BANCO DE DADOS ↧
def conecta_database():
    conexao = sql.connect('db_quitanda.db')
    conexao.row_factory = sql.Row
    return conexao
# INICIAR O BANCO E DADOS ↧
def iniciar_db():
    conexao = conecta_database()
    with app.open_resource('esquema.sql', mode='r') as comandos:
        # faz a leitura do arquivo sql
        conexao.cursor().executescript(comandos.read())
        conexao.commit()
        conexao.close()
# ROTA DA PÁGIA INICIAL ↧
@app.route('/')
def index():
    iniciar_db()
    conexao = conecta_database()
    produtos = conexao.execute('SELECT * FROM produtos ORDER BY id_prod DESC').fetchall
    conexao.close()
    title = 'Home'
    return render_template('home.html', produtos=produtos, title=title)
# FINAL DO CODIGO - EXECUTANDO O SERVIDOR
app.run(debug=True)
# caso nao colocado não é possivel ver os erros