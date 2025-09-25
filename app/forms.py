from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
from app.models import Usuario

class RegistroForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')
    
    def validate_username(self, username):
        user = Usuario.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nome de usuário já existe. Por favor, escolha outro.')

class LoginForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProdutoForm(FlaskForm):
    nome = StringField('Nome do Produto', validators=[DataRequired()])
    descricao = StringField('Descrição')
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=0)])
    preco = FloatField('Preço', validators=[DataRequired(), NumberRange(min=0)])
    url_imagem = StringField("URL da imagem")
    submit = SubmitField('Salvar Produto')