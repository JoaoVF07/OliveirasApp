# view.py

from app import app, db
from flask import render_template, url_for, request, redirect, flash
from app.forms import contatoForm, Userform, LoginForm
from app.models import Contato, User
from sqlalchemy import asc
from flask_login import login_user, logout_user, current_user


@app.route('/', methods=['GET','POST'])
def homepage():
    form = LoginForm()
    dados = Contato.query.order_by(Contato.data_marc.asc()).limit(5) # Chain order_by before all
    contato = Contato.query.order_by(Contato.data_marc.asc()).limit(5).all()
    context = {'dados': dados.all()}
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True) 


    return render_template('inicio.html', form=form, context=context, contato=contato)

   

@app.route('/cadastro/', methods=['GET','POST'])
def cadastro():
    form = Userform()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('cadastro.html', form=form)

@app.route('/sair/')
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/contato/', methods=['GET', 'POST'])
def contato():
    form = contatoForm()
    if form.validate_on_submit():
        form.save(current_user.id) 
        return redirect(url_for('contatoLista'))
    return render_template('contato.html', form=form)
    

@app.route('/contato/lista/', methods=['GET', 'POST'])
def contatoLista():
    if request.method == 'POST':
        contato_id = request.form.get('contato_id')
        contato_item = Contato.query.get(contato_id)
        if contato_item:
            contato_item.feito = not contato_item.feito
            db.session.commit()
    
    contato = Contato.query.order_by(Contato.data_marc.asc()).all()
    return render_template('contato_lista.html', contato=contato)


@app.route('/contato/<int:id>', methods=['GET', 'POST'])
def contatoDetail(id):
    obj = Contato.query.get(id)
    return render_template('contato_detail.html', obj=obj)
