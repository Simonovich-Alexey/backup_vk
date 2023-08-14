import sqlite3
import os
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ksajdgajglaaffakgnanadsj'

menu = [{'name': 'Главная страница', 'url': '/'},
        {'name': 'Про Flask', 'url': 'about'},
        {'name': 'Контакты', 'url': 'contacts'}]


@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html', title='Главная страница', menu=menu)


@app.route("/about")
def about():
    return render_template('about.html', menu=menu)


@app.route("/contacts", methods=["POST", "GET"])
def contacts():
    if request.method == 'POST':
        if len(request.form['name']) > 2:
            flash('Сообщение отправлено', category='flash__msg-success')
        else:
            flash('Ошибка отправки', category='flash__msg-error')

    return render_template('contacts.html', title='Контакты', menu=menu)


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"Профиль пользователя: {username}"


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'simonalex' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title="Авторизация", menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu), 404


if __name__ == '__main__':
    app.run(debug=True)
