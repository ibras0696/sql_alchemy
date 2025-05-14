# db.py — подключение к базе данных

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Адрес подключения к SQLite через асинхронный драйвер
# Здесь создаётся файл 'mydb.db' в текущей папке
DATABASE_URL = "sqlite+aiosqlite:///./mydb.db"

# Создаём асинхронный движок SQLAlchemy
# echo=True — выводит SQL-запросы в консоль (удобно для отладки)
engine = create_async_engine(DATABASE_URL)

# Создаём фабрику асинхронных сессий
# Сессия — это объект, через который мы взаимодействуем с БД
async_session = sessionmaker(
    bind=engine,                 # Привязываем движок к сессии
    class_=AsyncSession,        # Используем асинхронную версию сессии
    expire_on_commit=False      # Данные не сбрасываются после commit
)

# Создаём базовый класс для будущих моделей
# Все таблицы будут наследовать этот класс
Base = declarative_base()
