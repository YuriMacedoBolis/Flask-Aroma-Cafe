from flask import render_template, redirect, url_for, flash , session
from flask_login import login_user, logout_user, login_required , current_user
from app import app, db, bcrypt
from app.models import Usuario, Produto , Pedido , ItemPedido
from app.forms import RegistroForm, LoginForm, ProdutoForm
from functools import wraps
from datetime import datetime

#FUNCIONARIO
def funcionario_required(f):
    @wraps(f)
    def decorated_function(*args , **kwargs):
        if not current_user.is_funcionario:
            flash('Você nao tem permissao para acessar essa pátina' , 'danger')
            return redirect(url_for('homepage'))
        return f(*args , **kwargs)
    return decorated_function
            

#REGISTRAR NOVO USUÁRIO
@app.route("/registrar", methods=['GET', 'POST'])
def registrar():
    form = RegistroForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Usuario(username=form.username.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Sua conta foi criada! Agora você pode fazer o login.', 'success')
        return redirect(url_for('login'))
    flash("O Nome de Usuário já está em uso, por favor escolha outro nome." , 'danger')
    return render_template('registro.html', form=form)


#LOGIN 
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Login inválido. Verifique seu nome de usuário e senha.', 'danger')
    return render_template('login.html', form=form)

#LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    flash("Logout bem Sucedido, Até uma próxima!" , 'success')
    return redirect(url_for('homepage'))


#HOMEPAGE - PRINCIPAL
@app.route('/')
def homepage():
    return render_template('homepage.html')


#CARDAPIO
@app.route('/cardapio')
def cardapio():
    produtos = Produto.query.order_by(Produto.nome).all()
    return render_template('cardapio.html' , produtos = produtos)

#ADICIONAR AO CARRINHO
@app.route('/adicionar-ao-carrinho/<int:produto_id>' , methods=["POST"])
def adicionar_ao_carrinho(produto_id):
    if 'carrinho' not in session:
        session['carrinho'] = []
        
    session['carrinho'].append(produto_id)
    flash('produto adicionado com sucesso!' , 'success')
    return redirect(url_for('cardapio'))

#CARRINHO
@app.route('/carrinho')
def carrinho():
    if 'carrinho' in session:
        ids_produtos_no_carrinho = session['carrinho']
        produtos_no_carrinho = Produto.query.filter(Produto.id.in_(ids_produtos_no_carrinho))
        return render_template('carrinho.html' , produtos = produtos_no_carrinho)
    else:
        return render_template('carrinho.html' , produtos= [])
    

#FINALIZAR PEDIDO   
@app.route('/finalizar-pedido', methods=['POST'])
@login_required 
def finalizar_pedido():
    if 'carrinho' not in session or not session['carrinho']:
        flash('Seu carrinho está vazio!', 'danger')
        return redirect(url_for('cardapio'))
    
    novo_pedido = Pedido(
        usuario_id=current_user.id,
        data_pedido=datetime.utcnow(),
        status='Processando',
    )
    db.session.add(novo_pedido)
    db.session.commit()

    for produto_id in session['carrinho']:
        produto = Produto.query.get(produto_id)
        if produto:
            item = ItemPedido(
                quantidade=1,
                preco_unitario=produto.preco,
                pedido_id=novo_pedido.id,
                produto_id=produto.id
            )
            db.session.add(item)
    
    db.session.commit()
    
    session.pop('carrinho', None)
    
    flash('Pedido finalizado com sucesso!', 'success')
    return redirect(url_for('homepage'))


#HISTÓRICO DE PEDIDOS
@app.route('/meus_pedidos')
@login_required
def meus_pedidos():
    pedidos = Pedido.query.filter_by(usuario_id = current_user.id).order_by(Pedido.data_pedido.desc()).all()
    return render_template('historico_pedidos.html' , pedidos = pedidos)
    

#ESTOQUE
@app.route('/estoque')
@login_required
@funcionario_required
def estoque():
    produtos = Produto.query.order_by('nome').all()
    return render_template('estoque.html', produtos=produtos)

#FORM PARA ADICIONAR PRODUTOS
@app.route('/produto/add', methods=['GET', 'POST'])
@login_required
@funcionario_required
def add_produto():
    form = ProdutoForm()
    if form.validate_on_submit():
        novo_produto = Produto(
            nome=form.nome.data,
            preco=form.preco.data,
            quantidade=form.quantidade.data,
            descricao=form.descricao.data,
            url_imagem = form.url_imagem.data
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('estoque'))
    return render_template('add_produto.html', form=form)

#FORM PARA EDITAR PRODUTOS
@app.route('/produto/editar/<int:produto_id>' , methods=["GET" , "POST"])
@login_required
@funcionario_required
def editar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    form = ProdutoForm(obj=produto)
    
    if form.validate_on_submit():
        produto.nome = form.nome.data
        produto.preco = form.preco.data
        produto.quantidade = form.quantidade.data
        produto.descricao = form.descricao.data
        produto.url_imagem = form.url_imagem.data
        db.session.commit()
        flash('Produto Atualizado com sucesso!' , 'success')
        return redirect(url_for('estoque'))
    
    return render_template('editar_produto.html' , form=form , produto = produto)

# EXCLUIR PRODUTOS
@app.route('/produto/delete/<int:produto_id>', methods=['POST'])
@login_required
@funcionario_required
def deletar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('estoque'))