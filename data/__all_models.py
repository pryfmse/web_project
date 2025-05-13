import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


# Модель для зарегистрированных пользователей
class Reg(SqlAlchemyBase, UserMixin):
    __tablename__ = 'registered'

    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True,
                           autoincrement=True)  # Уникальный идентификатор (не первичный ключ)
    login = sqlalchemy.Column(sqlalchemy.String, primary_key=True, nullable=False,
                              unique=True)  # Логин как основной ключ
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # Хэшированный пароль
    status = sqlalchemy.Column(sqlalchemy.String,
                               nullable=False)  # Роль/статус пользователя (например, student, teacher)
    children = sqlalchemy.Column(sqlalchemy.String)  # Связь с детскими аккаунтами (для родительских учеток)


# Модель для хранения математических заданий
class MathTasks(SqlAlchemyBase):
    __tablename__ = 'math_tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # Уникальный ID задания
    number = sqlalchemy.Column(sqlalchemy.Integer)  # Номер задания в системе
    task_text = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # Текст задания
    task_picture = sqlalchemy.Column(sqlalchemy.LargeBinary)  # Изображение к заданию (опционально)
    answer = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # Ожидаемый ответ


# Модель для хранения заданий по информатике
class InfTasks(SqlAlchemyBase):
    __tablename__ = 'inf_tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # Уникальный ID задания
    number = sqlalchemy.Column(sqlalchemy.Integer)  # Номер задания в системе
    task_text = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # Текст задания
    task_picture = sqlalchemy.Column(sqlalchemy.LargeBinary)  # Изображение к заданию (опционально)
    file = sqlalchemy.Column(sqlalchemy.String)  # Прикрепленный файл (например, входные данные)
    file2 = sqlalchemy.Column(sqlalchemy.String)  # Дополнительный файл
    answer = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # Ожидаемый ответ


# Модель для хранения результатов по информатике (по пользователям)
class InfResults(SqlAlchemyBase):
    __tablename__ = 'inf_res'
    login = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("registered.login"),
                              primary_key=True)  # Связь с пользователем

    # Поля для хранения статусов выполнения заданий (0/1 или другие значения)
    t1 = sqlalchemy.Column(sqlalchemy.String, default=0)
    t2 = sqlalchemy.Column(sqlalchemy.String, default=0)
    # ... (аналогичные поля до t27b)

    reg = orm.relationship('Reg')  # Связь ORM с пользователем


# Модель для хранения результатов по математике (по пользователям)
class MathResults(SqlAlchemyBase):
    __tablename__ = 'math_res'
    login = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("registered.login"),
                              primary_key=True)  # Связь с пользователем

    # Поля для хранения статусов выполнения заданий
    t1 = sqlalchemy.Column(sqlalchemy.String, default=0)
    # ... (аналогичные поля до t12)

    reg = orm.relationship('Reg')  # Связь ORM с пользователем


# Модель для хранения вариантов и баллов пользователей
class Variant(SqlAlchemyBase):
    __tablename__ = 'variant'
    login = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("registered.login"),
                              primary_key=True)  # Связь с пользователем
    obj = sqlalchemy.Column(sqlalchemy.String)  # Выбранный предмет/вариант
    ball1 = sqlalchemy.Column(sqlalchemy.Integer, default=0)  # Накопленные баллы

    reg = orm.relationship('Reg')  # Связь ORM с пользователем