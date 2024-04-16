from flask_login import login_required, logout_user, LoginManager, login_user, current_user

from data import db_session
from flask import Flask, render_template, request, redirect
from data import __all_models

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    print(db_sess.get(__all_models.Reg, 1))
    return db_sess.get(__all_models.Reg, 1)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/reg_user', methods=['POST', 'GET'])
def reg_user():
    if request.method == 'GET':
        return render_template('reg_user.html')
    elif request.method == 'POST':
        session = db_session.create_session()
        for _ in session.query(__all_models.Reg).filter(__all_models.Reg.login == request.form['login']):
            return render_template('reg_user.html', mess='Этот пользователь уже зарегистрирован')
        session = db_session.create_session()
        user = __all_models.Reg()
        user.login = request.form['login']
        user.password = request.form['password']
        user.status = 'user'

        session.add(user)
        session.commit()
        login_user(user, remember=True)
        return redirect(f'/res_user_inf')


@app.route('/reg_admin', methods=['POST', 'GET'])
def reg_admin(mess=False):
    if request.method == 'GET':
        return render_template('reg_admin.html', mess=mess)
    elif request.method == 'POST':
        if request.form['key'] == app.config['SECRET_KEY']:
            session = db_session.create_session()
            for _ in session.query(__all_models.Reg).filter(__all_models.Reg.login == request.form['login']):
                return render_template('reg_admin.html', mess='Этот пользователь уже зарегистрирован')
            user = __all_models.Reg()
            user.login = request.form['login']
            user.password = request.form['password']
            user.status = 'admin'

            session.add(user)
            session.commit()
            login_user(user, remember=True)
            return redirect(f'/res_admin_inf')
        else:
            return render_template('reg_admin.html', mess='Неверный ключ')


@app.route('/enter', methods=['POST', 'GET'])
def enter(mess=False):
    if request.method == 'GET':
        return render_template('enter.html', mess=mess)
    elif request.method == 'POST':
        session = db_session.create_session()
        for _ in session.query(__all_models.Reg).filter(__all_models.Reg.login == request.form['login'],
                                                        __all_models.Reg.password == request.form['password']):
            user = session.query(__all_models.Reg).filter(__all_models.Reg.login == request.form['login']).first()
            login_user(user, remember=True)
            return redirect('/inf_main')
        else:
            return render_template('enter.html', mess='Не удалось войти')


@app.route('/res_user_inf')
def res_user_inf():
    print(current_user)
    session = db_session.create_session()
    print(session.query(__all_models.InfResults).filter(__all_models.InfResults.login == current_user.login))
    return render_template('res_user_inf.html', user=current_user)


@app.route('/res_user_math')
def res_user_math():
    return render_template('res_user_math.html', user=current_user)


@app.route('/res_admin_math', methods=['POST', 'GET'])
def res_admin1():
    if request.method == 'GET':
        return render_template('res_admin_math.html', user=current_user)
    elif request.method == 'POST':
        session = db_session.create_session()
        task = __all_models.MathTasks()
        task.number = request.form['number']
        task.task_text = request.form['text']
        if request.files['picture']:
            f = request.files['picture']
            task.task_picture = f.read()
        task.answer = request.form['answer']
        session.add(task)
        session.commit()
        return render_template('res_admin_math.html', user=current_user)


@app.route('/res_admin_inf', methods=['POST', 'GET'])
def res_admin2():
    if request.method == 'GET':
        return render_template('res_admin_inf.html', user=current_user)
    elif request.method == 'POST':
        session = db_session.create_session()
        task = __all_models.InfTasks()
        task.number = request.form['number']
        task.task_text = request.form['text']
        if request.files['picture']:
            f = request.files['picture']
            task.task_picture = f.read()
        if request.files['file']:
            f = request.files['file']
            task.file = f.read()
        if request.files['file2']:
            f = request.files['file2']
            task.file2 = f.read()
        task.answer = request.form['answer']
        session.add(task)
        session.commit()
        return render_template('res_admin_inf.html', user=current_user)


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


#             with open('data.png', 'wb') as file:
#                 file.write(self.foto[0])

# if current_user.is_authenticated: