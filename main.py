from data import db_session
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    return render_template('main.html')


def main():
    db_session.global_init("db/data.db")
    app.run()


if __name__ == '__main__':
    main()