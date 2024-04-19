import sqlalchemy
from flask_login import login_required, logout_user, LoginManager, login_user, current_user

from data import db_session
from flask import Flask, render_template, request, redirect
from data import __all_models

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
trans_inf = {0: 0, 1: 7, 2: 14, 3: 20, 4: 27, 5: 34, 6: 40, 7: 43, 8: 46, 9: 48, 10: 51, 11: 54, 12: 56,
             13: 59, 14: 62, 15: 64, 16: 67, 17: 70, 18: 72, 19: 75, 20: 78, 21: 80, 22: 83, 23: 85,
             24: 88, 25: 90, 26: 93, 27: 95, 28: 98, 29: 100}
trans_math = {0: 0, 1: 6, 2: 11, 3: 17, 4: 22, 5: 27, 6: 34, 7: 40, 8: 46, 9: 52, 10: 58, 11: 64, 12: 70}


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    query = db_sess.query(__all_models.Reg).filter(__all_models.Reg.id == sqlalchemy.text(user_id))
    results = list(db_sess.execute(query))[0][0]
    return results


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
        user_inf = __all_models.InfResults()
        user_math = __all_models.MathResults()
        user_math.login = request.form['login']
        user_inf.login = request.form['login']
        user.login = request.form['login']
        user.password = request.form['password']
        user.status = 'user'

        session.add(user)
        session.add(user_inf)
        session.add(user_math)
        session.commit()
        login_user(user)
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
            login_user(user)
            return redirect(f'/res_admin_inf')
        else:
            return render_template('reg_admin.html', mess='Неверный ключ')


@app.route('/enter', methods=['POST', 'GET'])
def enter(mess=False):
    if current_user.is_authenticated:
        if current_user.status == 'user':
            return redirect('/res_user_inf')
        elif current_user.status == 'admin':
            return redirect('/res_admin_inf')
    else:
        if request.method == 'GET':
            return render_template('enter.html', mess=mess)
        elif request.method == 'POST':
            session = db_session.create_session()
            for _ in session.query(__all_models.Reg).filter(__all_models.Reg.login == request.form['login'],
                                                            __all_models.Reg.password == request.form['password']):
                user = session.query(__all_models.Reg).filter(__all_models.Reg.login == request.form['login']).first()
                login_user(user)
                if current_user.status == 'user':
                    return redirect('/res_user_inf')
                elif current_user.status == 'admin':
                    return redirect('/res_admin_inf')
            else:
                return render_template('enter.html', mess='Не удалось войти')


@app.route('/res_user_inf')
def res_user_inf():
    db_sess = db_session.create_session()
    query = db_sess.query(__all_models.InfResults).filter(__all_models.InfResults.login == current_user.login)
    results = list(db_sess.execute(query))[0][0]
    n = len(list(filter(lambda x: x >= 70, [results.t1, results.t2, results.t3, results.t4, results.t5, results.t6,
                                            results.t7, results.t8, results.t9, results.t10, results.t11, results.t12,
                                            results.t13, results.t14, results.t15, results.t16, results.t17,
                                            results.t18, results.t19, results.t20, results.t21, results.t22, results.t23,
                                            results.t24, results.t25, results.t26a, results.t26b, results.t27a,
                                            results.t27b])))
    return render_template('res_user_inf.html', user=results, n_1=n, n_2=trans_inf[n])


@app.route('/res_user_math')
def res_user_math():
    db_sess = db_session.create_session()
    query = db_sess.query(__all_models.MathResults).filter(__all_models.MathResults.login == current_user.login)
    results = list(db_sess.execute(query))[0][0]
    n = len(list(filter(lambda x: x >= 70, [results.t1, results.t2, results.t3, results.t4, results.t5, results.t6,
                                            results.t7, results.t8, results.t9, results.t10, results.t11, results.t12])))
    return render_template('res_user_math.html', user=results, n_1=n, n_2=trans_math[n])


@app.route('/res_admin_math', methods=['POST', 'GET'])
def res_admin1():
    session = db_session.create_session()
    if request.method == 'GET':
        if current_user.children:
            table = []
            graphik = [[], [], [], [], [], [], [], [], [], [], [], []]
            for i in current_user.children.split():
                query = session.query(__all_models.InfResults).filter(__all_models.InfResults.login == i)
                results = list(session.execute(query))[0][0]
                n = [results.t1, results.t2, results.t3, results.t4, results.t5, results.t6,
                     results.t7, results.t8, results.t9, results.t10, results.t11, results.t12]
                for j in range(len(graphik)):
                    graphik[j].append(n[j])
                query = session.query(__all_models.Variant).filter(__all_models.Variant.login == i)
                if list(session.execute(query)):
                    table.append((i, sum(n) // 12, list(session.execute(query))))
                else:
                    table.append((i, sum(n) // 12, 0))
            graphik = [sum(k) // len(k) for k in graphik]
            return render_template('res_admin_math.html', user=current_user, table=table, graphik=graphik)
        else:
            return render_template('res_admin_math.html', user=current_user, table=[], graphik=[0, 0, 0, 0, 0,
                                                                                                0, 0, 0, 0, 0, 0, 0])
    elif request.method == 'POST':
        if request.form['log']:
            if current_user.children:
                current_user.children += ' ' + request.form['log']
            else:
                current_user.children = request.form['log']
            session.merge(current_user)
            session.commit()
            return render_template('res_admin_math.html', user=current_user)
        else:
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
    session = db_session.create_session()
    if request.method == 'GET':
        if current_user.children:
            table = []
            graphik = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                       [], [], [], [], [], [], [], [], [], [], [], []]
            for i in current_user.children.split():
                query = session.query(__all_models.InfResults).filter(__all_models.InfResults.login == i)
                results = list(session.execute(query))[0][0]
                n = [results.t1, results.t2, results.t3, results.t4, results.t5, results.t6,
                     results.t7, results.t8, results.t9, results.t10, results.t11, results.t12,
                     results.t13, results.t14, results.t15, results.t16, results.t17,
                     results.t18, results.t19, results.t20, results.t21, results.t22, results.t23,
                     results.t24, results.t25, results.t26a, results.t26b, results.t27a,
                     results.t27b]
                for j in range(len(graphik)):
                    graphik[j].append(n[j])
                query = session.query(__all_models.Variant).filter(__all_models.Variant.login == i)
                if list(session.execute(query)):
                    table.append((i, sum(n) // 29, list(session.execute(query))))
                else:
                    table.append((i, sum(n) // 29, 0))
            graphik = [sum(k) // len(k) for k in graphik]
            return render_template('res_admin_inf.html', user=current_user, table=table, graphik=graphik)
        else:
            return render_template('res_admin_inf.html', user=current_user, table=[], graphik=[0, 0, 0, 0, 0, 0, 0,
                                                                                               0, 0, 0, 0, 0, 0, 0,
                                                                                               0, 0, 0, 0, 0, 0, 0,
                                                                                               0, 0, 0, 0, 0, 0, 0, 0])
    elif request.method == 'POST':
        if request.form['log']:
            if current_user.children:
                current_user.children += ' ' + request.form['log']
            else:
                current_user.children = request.form['log']
            session.merge(current_user)
            session.commit()
            return render_template('res_admin_math.html', user=current_user)
        else:
            session = db_session.create_session()
            task = __all_models.InfTasks()
            task.number = request.form['number']
            task.task_text = request.form['text']
            if request.files['picture']:
                f = request.files['picture']
                task.task_picture = f.read()
            task.file = request.form['file']
            task.file2 = request.form['file2']
            task.answer = request.form['answer']
            session.add(task)
            session.commit()
            return render_template('res_admin_inf.html', user=current_user)


@app.route('/math_main')
def math_main():
    return render_template('math_main.html')


@app.route('/inf_main', methods=['GET', 'POST'])
def inf_main():
    print(request.form.getlist('inf'))
    print(1)
    return render_template('inf_main.html')
    # for i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14',
    #           '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27']


@app.route('/decision', methods=['GET', 'POST'])
def decision():
    if request.method == 'GET':
        return render_template('decision.html')
    if request.method == 'POST':
        return 'ok'


def main():
    db_session.global_init("db/data.db")
    app.run()


if __name__ == '__main__':
    main()


#             with open('data.png', 'wb') as file:
#                 file.write(self.foto[0])

# if current_user.is_authenticated: