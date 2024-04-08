from data import db_session
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/reg_user', methods=['POST', 'GET'])
def reg_user():
    if request.method == 'GET':
        return render_template('reg_user.html')
    elif request.method == 'POST':
        print(request.form['email'])
        print(request.form['password'])
        print(request.form['class'])
        print(request.form['file'])
        print(request.form['about'])
        print(request.form['accept'])
        print(request.form['sex'])
        f = request.files['file']
        print(f.read())
        return "Форма отправлена"


@app.route('/reg_admin', methods=['POST', 'GET'])
def reg_admin():
    if request.method == 'GET':
        return render_template('reg_admin.html')
    elif request.method == 'POST':
        if request.form['key'] == app.config['SECRET_KEY']:
            print(request.form['login'])
            print(request.form['password'])
            f = request.files['file']
            print(f.read())
            return "Форма отправлена"
        else:
            return 'Неверный ключ'


@app.route('/enter', methods=['POST', 'GET'])
def enter():
    if request.method == 'GET':
        return render_template('enter.html')
    elif request.method == 'POST':
        print(request.form['login'])
        print(request.form['password'])
        return res_user(request.form['login'])


@app.route('/res_user')
def res_user(name):
    return render_template('result_user.html', name=name)


@app.route('/res_admin')
def res_admin(name):
    return render_template('res_admin.html', name=name)


def main():
    db_session.global_init("db/data.db")
    app.run()


if __name__ == '__main__':
    main()