from data import db_session
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/reg_user', methods=['POST', 'GET'])
def reg_user():
    if request.method == 'GET':
        return render_template('reg_user.html')
    elif request.method == 'POST':  # добавлять фото, логин и пароль в базу данных. Открывать страницу профиля
        name = request.form['login']
        password = request.form['password']
        # if request.files['photo']:
        #     picture = request.files['photo']
        return redirect(f'/res_user/{name}')


@app.route('/reg_admin', methods=['POST', 'GET'])
def reg_admin():
    if request.method == 'GET':
        return render_template('reg_admin.html')
    elif request.method == 'POST':  # добавлять фото, логин и пароль в базу данных. Открывать страницу профиля
        if request.form['key'] == app.config['SECRET_KEY']:
            name = request.form['login']
            password = request.form['password']
            if request.files['file']:
                picture = request.form['file']
            return redirect(f'/res_admin/{name}')
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


@app.route('/res_user/<name>')
def res_user(name):
    return render_template('result_user.html', name=name)


@app.route('/res_admin')
def res_admin(name):
    return render_template('res_admin.html', name=name)


@app.route('/math_main')
def math_main():
    return render_template('math_main.html')


@app.route('/inf_main')
def inf_main():
    return render_template('inf_main.html')


def main():
    db_session.global_init("db/data.db")
    app.run()


if __name__ == '__main__':
    main()