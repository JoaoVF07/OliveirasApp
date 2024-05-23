from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    data_envio=db.Column(db.DateTime,default=datetime.now())
    nome=db.Column(db.String, nullable=True)
    email= db.Column(db.String, nullable=True)
    senha = db.Column(db.String, nullable=True)
    contato = db.relationship('Contato', backref='user', lazy=True)


class Contato(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    data_envio=db.Column(db.DateTime,default=datetime.now())
    nome=db.Column(db.String, nullable=True)
    data_marc = db.Column(db.Date, nullable=True) 
    feito = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)

