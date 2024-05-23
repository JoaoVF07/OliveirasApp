
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, DateField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


from app import db, bcrypt
from app.models import Contato, User


class contatoForm(FlaskForm):
    data_marc = DateField('Data', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self, user_id):
        contato = Contato( 
            user_id = user_id,
            data_marc = self.data_marc.data
        )
        db.session.add(contato)
        db.session.commit()

class Userform(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def validade_email(self, email):
        if User.query.filter(email=email.data).first():
            return ValidationError('Usuário já cadastrado com esse E-mail!!!')

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        user = User(
            nome = self.nome.data,
            email = self.email.data,
            senha = senha
        )
        db.session.add(user)
        db.session.commit()
        return user 

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(),Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Login')

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                return user
            else:
                raise Exception('Senha incorreta!')
        else:
            raise Exception('Usuário não encontrado!!!')

