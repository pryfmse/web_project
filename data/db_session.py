import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

# Базовый класс для декларативных моделей SQLAlchemy
SqlAlchemyBase = dec.declarative_base()

# Глобальная переменная для фабрики сессий
__factory = None


def global_init(db_file):
    global __factory

    # Если фабрика уже инициализирована, выходим из функции
    if __factory:
        return

    # Проверка наличия имени файла БД
    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    # Формирование строки подключения для SQLite
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    # Создание движка БД с отключенным эхо-выводом (echo=False)
    engine = sa.create_engine(conn_str, echo=False)
    # Инициализация фабрики сессий
    __factory = orm.sessionmaker(bind=engine)

    # Импорт моделей для автоматического создания таблиц
    # noinspection PyUnresolvedReferences
    from . import __all_models  # noqa

    # Создание всех таблиц в базе данных
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    """Создает и возвращает новую сессию работы с БД"""
    global __factory
    return __factory()