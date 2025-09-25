from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

# Tabela para os produtos da loja
class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    descricao = db.Column(db.Text , nullable = False)
    url_imagem = db.Column(db.String(200) , nullable = True)

# Tabela para os usuários
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    is_funcionario = db.Column(db.Boolean , default=False)

    def __repr__(self):
        return f"Usuario('{self.username}')"

#Tabela para pedidos
class Pedido(db.Model):
    __tablename__ = "pedidos"
    id = db.Column(db.Integer , primary_key = True)
    data_pedido = db.Column(db.DateTime , nullable = False , default = datetime.utcnow)
    status = db.Column(db.String(20) , nullable=False , default = "Pendente")
    total = db.Column(db.Float , nullable=False , default = 0.0)
    usuario_id = db.Column(db.Integer , db.ForeignKey('usuarios.id'), nullable=False)
    itens = db.relationship('ItemPedido',backref='pedidos',lazy=True)
    
# Tabela para os itens dentro de um pedido
class ItemPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    produto = db.relationship('Produto', backref='item_pedidos')

    def __repr__(self):
        return f"ItemPedido('{self.quantidade}', '{self.produto_id}')"

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
