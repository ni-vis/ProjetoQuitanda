from flask import Flask, render_template, request, redirect, session
# importando flask e todas as classes que vamos usar 
# chama o html(extend), redenriza pagina html (render_template)
# pega respostas e dados de um formulario (request)
# rota, função, apontando para uma rota que ja existe (redirect)
# chama sessao (session)
import sqlite3 as sql
import uuid
import os 
# serve para gerar nomes/numeros aleatorios unicos para as imagens, gera numeros aleatorios para concatenar com os nomes das imagens que serao utilizadas (uuid)
app = Flask(__name__)
app.secret_key = "quitandazezinho"
# salvar sessao e colocar ums especie de segruança (secrect_key)
usuario = 'u'
senha = 's'
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
    produtos = conexao.execute('SELECT * FROM produtos ORDER BY id_prod DESC').fetchall()
    conexao.close()
    title = 'home'
    return render_template('home.html', produtos=produtos, title=title)
# ROTA DA PÁGINA ACESSO ↧
@app.route("/acesso", methods=['post'])
def acesso():
    global usuario, senha
    usuario_informado = request.form["usuario"]
    senha_informada = request.form["senha"]
    if usuario == usuario_informado and senha == senha_informada:
        session["login"] = True
        return redirect('/adm')
    else:
        return render_template("login.html",msg="Usuário/Senha estão incorretos!")
#ROTA DA PÁGIA DE LOGIN ↧
@app.route("/login")
def login():
    return render_template("login.html")
#ROTA DA PÁGIA ADM ↧
@app.route("/adm")
def adm():
    if verifica_sessao():
        iniciar_db()
        conexao = conecta_database()
        produtos = conexao.execute( 'SELECT * FROM produtos ORDER BY id_prod DESC').fetchall()
        conexao.close()
        title = 'Administração'
        return render_template('adm.html', produtos=produtos, title=title)
    else:
        return redirect('/login')
def acesso():
    global usuario, senha
    usuario_informado = request.form["usuario"]
    senha_informada = request.form["senha"]
    if usuario == usuario_informado and senha == senha_informada:
        session["login"] = True
        return redirect('/adm')
    else:
        return render_template("login.html",msg="Usuário/Senha estão incorretos!")
# CÓDIGO DO LOGOUT ↧
@app.route('/logout')
def logout():
    global login
    login = False 
    session.clear()
    return redirect('/')
# ROTA DA PÁGINA DE CADASTRO ↧
@app.route('/cadprodutos')
def cadprodutos():
    if verifica_sessao():
        title = 'Cadastro de produtos'
        return render_template("cadastro.html", title=title)
    else:
        return redirect('/login')
# ROTA DA PAGINA DE CADASTRO NO BANCO ↧
@app.route('/cadastro', methods=['post'])
def cadastro():
    if verifica_sessao():
        nome_prod=request.form['nome_prod']
        desc_prod=request.form['desc_prod']
        preco_prod=request.form['preco_prod']
        img_prod=request.files['img_prod']
        id_foto=str(uuid.uuid4().hex)
        filename=id_foto+nome_prod+'.png'
        img_prod.save('static/img/produtos/'+filename)
        conexao = conecta_database()
        conexao.execute('INSERT INTO produtos (nome_prod, desc_prod, preco_prod, img_prod) VALUES (?, ?, ?, ?)', (nome_prod, desc_prod, preco_prod, filename))
        conexao.commit()
        conexao.close()
        return redirect('/adm')
    else:
        return redirect('/login')
@app.route("/sobre")
def login_page():
    return render_template("sobre.html")
# ROTA PARA TRATAR A EDIÇÃO
@app.route("/editarprodutos", methods=['POST'])
def editar_prod():
    id_prod = request.form['id_prod']
    nome_prod = request.form['nome_prod']
    desc_prod = request.form['desc_prod']
    preco_prod = request.form['preco_prod']
    img_prod = request.files['img_prod']

    id_foto = str(uuid.uuid4().hex)
    filename = id_foto + nome_prod + '.png'

    conexao = conecta_database()

    if img_prod:
        produto = conexao.execute('SELECT * FROM produtos WHERE id_prod = ?', (id_prod,)).fetchall()
        filename_old = produto[0]['img_prod']
        excluir_arquivo = "static/img/produtos" + filename_old
        os.remove(excluir_arquivo)
        img_prod.save("static/img/produtos/" + filename)
        conexao.execute('UPDATE produtos SET nome_prod = ?, desc_prod = ?, preco_prod = ?, img_prod = ? WHERE id_prod = ?', (nome_prod, desc_prod, preco_prod, filename, id_prod))
    else:
        conexao.execute('UPDATE produtos SET nome_prod = ?, desc_prod = ?, preco_prod = ? WHERE id_prod = ?', (nome_prod, desc_prod, preco_prod, id_prod))

    conexao.commit()
    conexao.close()

    return redirect('/adm')

# ROTA DE EXCLUSÃO
@app.route('/excluir/<id>')
def excluir(id):
    if verifica_sessao():
        id = int(id)
        conexao = conecta_database()
        produto = conexao.execute('SELECT * FROM produtos WHERE id_prod = ?', (id,)).fetchall()
        filename_old = produto[0]['img_prod']
        excluir_arquivo = "static/img/produtos" + filename_old
        os.remove(excluir_arquivo)
        conexao.execute('DELETE FROM produtos WHERE id_prod = ?', (id,))
        conexao.commit()
        conexao.close()
        return redirect('/adm')
    else:
        return redirect('/login')
 

# ROTA DE EDIÇÃO ↧   
@app.route('/editprodutos/<id_prod>')
def editar(id_prod):
    if verifica_sessao():
        iniciar_db()
        conexao = conecta_database()
        produtos = conexao.execute('SELECT * FROM produtos WHERE id_prod = ?', (id_prod,)).fetchall()
        conexao.close()
        title = 'Edição de Produtos'
        return render_template('editprodutos.html', produtos=produtos, title=title)
    else:
        return redirect('/login')
# ROTA PARA TRATAR DA EDIÇÃO ↧
@app.route('/editarprodutos', methods=['POST'])
def editprod():
    id_prod = request.form['id_prod']
    nome_prod = request.form['nome_prod']
    desc_prod = request.form['desc_prod']
    preco_prod = request.form['preco_prod']
    img_prod = request.files['img_prod']
    
    id_foto = str(uuid.uuid4().hex)
    filename = id_foto + nome_prod + '.png'
    
    img_prod.save('static/img/produtos/' + filename)
    
    conexao = conecta_database()
    conexao.execute('UPDATE produtos SET nome_prod = ?, desc_prod = ?, preco_prod = ?, img_prod = ? WHERE id_prod = ?', (nome_prod, desc_prod, preco_prod, filename, id_prod))
    conexao.commit()
    conexao.close()
    
    return redirect('/adm')
# ROTA DA PÁGINA DE BUSCA
@app.route('/busca', methods=['post'])
def busca():
    busca=request.form['buscar']
    conexao = conecta_database()
    produtos = conexao.execute('SELECT * FROM produtos WHERE nome_prod LIKE "%" || ? || "%"',(busca,)).fetchall()
    title = "Home"
    return render_template("home.html", produtos = produtos, title = title)
# FINAL DO CODIGO - EXECUTANDO O SERVIDOR ↧
app.run(debug=True)
# caso nao colocado não é possivel ver os erros