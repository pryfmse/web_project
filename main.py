from data import db_session
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/reg_user')
def reg_user():
    return render_template('reg_user.html')


@app.route('/reg_admin')
def reg_admin():
    return render_template('reg_admin.html')


@app.route('/enter')
def enter():
    return render_template('enter.html')


def main():
    db_session.global_init("db/data.db")
    app.run()


if __name__ == '__main__':
    main()