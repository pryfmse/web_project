from data import db_session
from flask import Flask, render_template, request, redirect
from data import __all_models

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/reg_user', methods=['POST', 'GET'])
def reg_user():
    if request.method == 'GET':
        return render_template('reg_user.html')
    elif request.method == 'POST':  # добавлять фото
        session = db_session.create_session()
        user = __all_models.Reg()
        user.login = request.form['login']
        user.password = request.form['password']
        user.status = 'user'

        session.add(user)
        session.commit()
        return redirect(f'/res_user_inf/{request.form["login"]}')


@app.route('/reg_admin', methods=['POST', 'GET'])
def reg_admin():
    if request.method == 'GET':
        return render_template('reg_admin.html')
    elif request.method == 'POST':  # добавлять фото в базу данных
        if request.form['key'] == app.config['SECRET_KEY']:
            session = db_session.create_session()
            user = __all_models.Reg()
            user.login = request.form['login']
            user.password = request.form['password']
            user.status = 'admin'

            session.add(user)
            session.commit()
            return redirect(f'/res_admin/{request.form["login"]}')
        else:
            return 'Неверный ключ'  # всплывающее окно


@app.route('/enter', methods=['POST', 'GET'])
def enter():
    if request.method == 'GET':
        return render_template('enter.html')
    elif request.method == 'POST':
        session = db_session.create_session()
        for i in session.query(__all_models.Reg).filter(__all_models.Reg.login == request.form['login'], __all_models.Reg.password == request.form['password']):
            return redirect('/inf_main')
        else:
            return 'Не удаётся войти'  # всплывающее окно


@app.route('/res_user_inf/<name>')
def res_user_inf(name):
    return render_template('res_user_inf.html', name=name)


@app.route('/res_user_math/<name>')
def res_user_math(name):
    return render_template('res_user_math.html', name=name)


@app.route('/res_admin/<name>')
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