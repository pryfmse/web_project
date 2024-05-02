from random import randint

import sqlalchemy
from flask_login import login_required, logout_user, LoginManager, login_user, current_user

from data import db_session
from flask import Flask, render_template, request, redirect
from data import __all_models

app = Flask(__name__)
flag = False
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
    results = [results.t1, results.t2, results.t3, results.t4, results.t5, results.t6,
               results.t7, results.t8, results.t9, results.t10, results.t11, results.t12,
               results.t13, results.t14, results.t15, results.t16, results.t17,
               results.t18, results.t19, results.t20, results.t21, results.t22, results.t23,
               results.t24, results.t25, results.t26a, results.t26b, results.t27a,
               results.t27b]
    for x in range(len(results)):
        m = list(map(int, results[x].split()))
        results[x] = int((sum(m) / len(m)) * 100)
    n = len(list(filter(lambda x: x >= 70, results)))
    return render_template('res_user_inf.html', user=results, n_1=n, n_2=trans_inf[n], prof=current_user.login)


@app.route('/res_user_math')
def res_user_math():
    db_sess = db_session.create_session()
    query = db_sess.query(__all_models.MathResults).filter(__all_models.MathResults.login == current_user.login)
    results = list(db_sess.execute(query))[0][0]
    results = [results.t1, results.t2, results.t3, results.t4, results.t5, results.t6,
               results.t7, results.t8, results.t9, results.t10, results.t11, results.t12]
    for x in range(len(results)):
        m = list(map(int, results[x].split()))
        results[x] = int((sum(m) / len(m)) * 100)
    n = len(list(filter(lambda x: x >= 70, results)))
    return render_template('res_user_math.html', user=results, n_1=n, n_2=trans_math[n], prof=current_user.login)


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
                for x in range(len(n)):
                    m = list(map(int, n[x].split()))
                    n[x] = int((sum(m) / len(m)) * 100)
                for j in range(len(graphik)):
                    graphik[j].append(n[j])
                query = session.query(__all_models.Variant).filter(__all_models.Variant.login == i)
                if list(session.execute(query)):
                    var = list(session.execute(query))[0][0]
                    if var.obj == 'math':
                        table.append((i, sum(n) // 12, var.ball1))
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
                for x in range(len(n)):
                    m = list(map(int, n[x].split()))
                    n[x] = int((sum(m) / len(m)) * 100)
                for j in range(len(graphik)):
                    graphik[j].append(n[j])
                query = session.query(__all_models.Variant).filter(__all_models.Variant.login == i)
                if list(session.execute(query)):
                    var = list(session.execute(query))[0][0]
                    if var.obj == 'inf':
                        table.append((i, sum(n) // 29, var.ball1))
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
            if request.form['file']:
                task.file = request.form['file']
            if request.form['file2']:
                task.file2 = request.form['file2']
            task.answer = request.form['answer']
            session.add(task)
            session.commit()
            return render_template('res_admin_inf.html', user=current_user)


@app.route('/math_main', methods=['GET', 'POST'])
def math_main():
    global flag
    if request.method == 'POST' and flag:
        flag = False
        return res('math')
    if request.method == 'POST':
        session = db_session.create_session()
        a = []
        photo = {}
        for i in request.form.getlist('math'):
            results = list(
                session.execute(session.query(__all_models.MathTasks).filter(__all_models.MathTasks.number == int(i))))
            k = results[randint(0, len(results)) - 1][0]
            if k.task_picture:
                with open('static/img/t' + str(k.number) + '.png', 'wb') as file:
                    file.write(k.task_picture)
                    photo[k.number] = 'static/img/t' + str(k.number) + '.png'
            a.append(k)
        flag = True
        return test('math', a, photo)
    return render_template('math_main.html')


@app.route('/inf_main', methods=['GET', 'POST'])
def inf_main():
    global flag
    if request.method == 'POST' and flag:
        flag = False
        return res('inf')
    if request.method == 'POST':
        session = db_session.create_session()
        a = []
        photo = {}
        for i in request.form.getlist('inf'):
            results = list(
                session.execute(session.query(__all_models.InfTasks).filter(__all_models.InfTasks.number == int(i))))
            k = results[randint(0, len(results)) - 1][0]
            if k.task_picture:
                with open('static/img/t' + str(k.number) + '.png', 'wb') as file:
                    file.write(k.task_picture)
                    photo[k.number] = 'static/img/t' + str(k.number) + '.png'
            a.append(k)
        flag = True
        return test('inf', a, photo)
    return render_template('inf_main.html')


@app.route('/decision_math', methods=["GET", "POST"])
def decision_m():
    global flag
    if request.method == 'POST' and flag:
        flag = False
        return res('math')
    session = db_session.create_session()
    a = []
    photo = {}
    for i in range(1, 13):
        results = list(
        session.execute(session.query(__all_models.MathTasks).filter(__all_models.MathTasks.number == i)))
        k = results[randint(0, len(results)) - 1][0]
        if k.task_picture:
            with open('static/img/t' + str(k.number) + '.png', 'wb') as file:
                file.write(k.task_picture)
                photo[k.number] = 'static/img/t' + str(k.number) + '.png'
        a.append(k)
    flag = True
    return test('math', a, photo)


@app.route('/decision_inf', methods=['GET', 'POST'])
def decision_i():
    global flag
    if request.method == 'POST' and flag:
        flag = False
        return res('inf')
    session = db_session.create_session()
    a = []
    photo = {}
    for i in range(1, 28):
        results = list(
            session.execute(session.query(__all_models.InfTasks).filter(__all_models.InfTasks.number == i)))
        k = results[randint(0, len(results)) - 1][0]
        if k.task_picture:
            with open('static/img/t' + str(k.number) + '.png', 'wb') as file:
                file.write(k.task_picture)
                photo[k.number] = 'static/img/t' + str(k.number) + '.png'
        a.append(k)
    flag = True
    return test('inf', a, photo)


def test(obj, a, photo):
    return render_template('decision.html', lst=a, object=obj, photo=photo)


def res(obj):
    session = db_session.create_session()
    res = []
    summ = 0
    if current_user.is_authenticated:
        if obj == 'math':
            query = session.query(__all_models.MathResults).filter(
                __all_models.MathResults.login == current_user.login)
            user = list(session.execute(query))[0][0]
            task = {'1': user.t1, '2': user.t2, '3': user.t3, '4': user.t4, '5': user.t5, '6': user.t6,
                    '7': user.t7, '8': user.t8, '9': user.t9, '10': user.t10, '11': user.t11, '12': user.t12}
        else:
            query = session.query(__all_models.InfResults).filter(
                __all_models.InfResults.login == current_user.login)
            user = list(session.execute(query))[0][0]
            task = {'1': user.t1, '2': user.t2, '3': user.t3, '4': user.t4, '5': user.t5, '6': user.t6,
                    '7': user.t7, '8': user.t8, '9': user.t9, '10': user.t10, '11': user.t11, '12': user.t12,
                    '13': user.t13, '14': user.t14, '15': user.t15, '16': user.t16, '17': user.t17, '18': user.t18,
                    '19': user.t19, '20': user.t20, '21': user.t21, '22': user.t22, '23': user.t23, '24': user.t24,
                    '25': user.t25, '26': user.t26a, '27': user.t27a}
    for i in request.form.keys():
        a, b = i.split('_')
        v = 1 if b == request.form[i] else 0
        summ += v
        res.append((a, v))
        if current_user.is_authenticated:
            k = task[a].split() + [str(v)]
            task[a] = ' '.join(k)
    if current_user.is_authenticated:
        if (obj == 'math' and len(res) == 12) or (obj == 'inf' and len(res) == 27):
            var = __all_models.Variant()
            var.login = current_user.login
            var.obj = obj
            var.ball1 = summ
            session.add(var)
            session.add(user)
            session.commit()
    return render_template('res.html', res=res, itog=summ)


@app.route('/motivation')
def mot():
    return render_template('motivation.html')


@app.route('/lifehack')
def lifeh():
    return render_template('lifeh.html')


def main():
    db_session.global_init("db/data.db")
    app.run()


if __name__ == '__main__':
    main()
