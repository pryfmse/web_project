import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Reg(SqlAlchemyBase):
    __tablename__ = 'registered'

    login = sqlalchemy.Column(sqlalchemy.String, primary_key=True, nullable=False, unique=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class MathTasks(SqlAlchemyBase):
    __tablename__ = 'math_tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    task_text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    task_picture = sqlalchemy.Column(sqlalchemy.LargeBinary)
    answer = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class InfTasks(SqlAlchemyBase):
    __tablename__ = 'inf_tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    task_text = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    task_picture = sqlalchemy.Column(sqlalchemy.LargeBinary)
    file = sqlalchemy.Column(sqlalchemy.LargeBinary)
    answer = sqlalchemy.Column(sqlalchemy.String, nullable=False)


class InfResults(SqlAlchemyBase):
    __tablename__ = 'inf_res'
    login = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("registered.login"), primary_key=True)
    t1 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t2 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t3 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t4 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t5 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t6 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t7 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t8 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t9 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t10 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t11 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t12 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t13 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t14 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t15 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t16 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t17 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t18 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t19 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t20 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t21 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t22 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t23 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t24 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t25 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t26a = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t26b = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t27a = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t27b = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    reg = orm.relationship('Reg')


class MathResults(SqlAlchemyBase):
    __tablename__ = 'math_res'
    login = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("registered.login"), primary_key=True)
    t1 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t2 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t3 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t4 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t5 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t6 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t7 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t8 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t9 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t10 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t11 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    t12 = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    reg = orm.relationship('Reg')


class Variant(SqlAlchemyBase):
    __tablename__ = 'variant'
    login = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("registered.login"), primary_key=True)
    ball1 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    ball2 = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    reg = orm.relationship('Reg')