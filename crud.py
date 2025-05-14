# crud.py — функции для взаимодействия с базой данных (CRUD)
import asyncio

from sqlalchemy import select
from db import async_session
from models import User, Post

# Создание нового пользователя
async def add_user(name: str, age: int):
    async with async_session() as session:
        user = User(name=name, age=age)  # Создаём объект User
        session.add(user)                # Добавляем в сессию
        await session.commit()           # Сохраняем изменения в БД

# Получение всех пользователей
async def get_all_users():
    async with async_session() as session:
        result = await session.execute(select(User))  # SELECT * FROM users
        return result.scalars().all()  # Возвращаем список пользователей

# Обновление возраста пользователя по ID
async def update_user_age(user_id: int, new_age: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()  # Получаем одного пользователя или None
        if user:
            user.age = new_age              # Меняем возраст
            await session.commit()          # Сохраняем

# Удаление пользователя по ID
async def delete_user(user_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            await session.delete(user)     # Удаляем объект
            await session.commit()

# Получить пользователей, у которых есть посты (JOIN)
async def get_users_with_posts():
    async with async_session() as session:
        result = await session.execute(select(User).join(User.posts))
        return result.scalars().all()


# 1 Задача
'''
    Добавь несколько пользователей в базу
    ➤ Создай функцию 
        add_many_users(users: list[tuple[str, int]]) и добавь пачку пользователей.
'''
async def add_many_users(users: list[tuple[str, int]]):
    async with async_session() as session:
        lst_users = [User(name=name, age=age) for name, age in users]
        session.add_all(lst_users)
        await session.commit()


# 2 Задача
'''
    Получи всех пользователей, которым больше 18 лет
    ➤ Используй 
        select().where(User.age > 18) и выведи имена.
'''
async def get_where_age_user(age: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.age >= age))
        return result.scalars().all()


# 3 Задача
'''
    Найди пользователя по имени (точное совпадение)
    ➤ Функция       
        get_user_by_name(name: str) должна вернуть объект User или None.
'''
async def get_user_by_name(name: str):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.name == name))
        return result.scalars().first()


# result = asyncio.run(get_user_by_name('Ибра'))
#
# print(result.to_dict())



# 4 Задача
'''
    Проверь, существует ли пользователь с ID = N
        ➤ Верни True или False.
'''







# 5 Задача
'''
    Добавь пользователю пост
    ➤ Создай функцию 
        add_post(user_id: int, title: str) — пост должен связаться через ForeignKey.
'''
async def add_post(user_id: int, title: str):
    async with async_session() as session:
        session.add(Post(title=title, user_id=user_id))
        await session.commit()

async def get_post(user_id: int):
    async with async_session() as session:
        result = await session.execute(select(Post).where(Post.user_id == user_id))
        return result.scalars().all()

print(asyncio.run(add_post(3, 'Привет, это пост')))
print(asyncio.run(get_post(3)))
# asyncio.run(add_many_users(
#     [
#         ('Ибра', 18),
#         ('Иу', 54),
#
#     ]
# ))
# result = asyncio.run(get_where_age_user(18))
#
# for elem in result:
#     print(elem.to_dict())

'''
    Что выбираешь	Как получить результат
        Один объект (User)	= .scalars().first() или .scalar_one_or_none()
        Все объекты	        = .scalars().all()
        Несколько колонок	= .all()
'''