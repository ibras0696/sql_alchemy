# models.py — описание таблиц базы данных

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

# Таблица пользователей
class User(Base):
    __tablename__ = 'users'  # Название таблицы в базе

    id = Column(Integer, primary_key=True)  # Уникальный ID (ключ)
    name = Column(String)                   # Имя пользователя
    age = Column(Integer)                  # Возраст пользователя

    # Связь: один пользователь -> много постов
    posts = relationship("Post", back_populates="user")

    def __str__(self):
        return f'Имя: {self.name} Возраст: {self.age}'

    def to_dict(self):
        return {
            self.id: {
                'name': self.name,
                'age': self.age
            },

        }
# Таблица постов
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)      # Уникальный ID поста
    title = Column(String)                      # Название поста
    user_id = Column(Integer, ForeignKey('users.id'))  # Внешний ключ на user.id

    # Обратная связь: каждый пост связан с пользователем
    user = relationship("User", back_populates="posts")

#
# async def get_all_users():
#     async with async_session() as session:
#         result = await session.execute(select(User))  # SELECT * FROM users
# #         return result.scalars().all()  # Возвращаем список пользователей




















# async def add_many_users(users: list[tuple[str, int]]):
#     async with async_session() as session:
#         lst_users = [User(name=name, age=age) for name, age in users]
#         session.add_all(lst_users)
#         await session.commit()
























