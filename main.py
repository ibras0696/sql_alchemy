# main.py — точка входа в программу

import asyncio
from db import engine, Base  # Импортируем движок и базу для создания таблиц
from crud import add_user, get_all_users, update_user_age, delete_user

# Функция для создания всех таблиц в базе
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Создаём таблицы

# Главная функция для тестирования CRUD-операций
async def main():
    await init_db()  # Сначала создаём таблицы

    # Добавляем пользователя
    await add_user("Смитти", 25)

    # Получаем всех пользователей и выводим их
    users = await get_all_users()
    for user in users:
        print(f"{user.id}: {user.name}, {user.age} лет")

    # Обновляем возраст первого пользователя
    await update_user_age(1, 30)

    # Удаляем первого пользователя
    await delete_user(1)

# Запускаем event loop
asyncio.run(main())
