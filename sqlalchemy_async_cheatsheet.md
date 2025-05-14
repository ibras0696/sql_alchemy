
# 🐍 SQLAlchemy Async ORM — Шпаргалка от Смитти

---

## 📦 Подключение к базе данных

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./mydb.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()
```

---

## 🧱 Создание моделей

```python
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    posts = relationship("Post", back_populates="user")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "age": self.age}

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")
```

---

## 🛠️ Создание таблиц

```python
async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

---

## 📥 Добавление данных

```python
# Один пользователь
async def add_user(name: str, age: int):
    async with async_session() as session:
        session.add(User(name=name, age=age))
        await session.commit()

# Несколько пользователей
async def add_many_users(users: list[tuple[str, int]]):
    async with async_session() as session:
        session.add_all([User(name=name, age=age) for name, age in users])
        await session.commit()
```

---

## 🔍 Получение данных

```python
# Все пользователи
result = await session.execute(select(User))
users = result.scalars().all()

# Один по условию
result = await session.execute(select(User).where(User.name == "Смитти"))
user = result.scalars().first()

# Один строго (ошибка, если нет)
result = await session.execute(select(User).where(User.id == 1))
user = result.scalar_one()

# Один или None
user = result.scalar_one_or_none()
```

---

## 🔄 Обновление данных

```python
async def update_user_name(user_id: int, new_name: str):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            user.name = new_name
            await session.commit()
```

---

## ❌ Удаление данных

```python
async def delete_user(user_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            await session.delete(user)
            await session.commit()
```

---

## 🔗 Отношения и JOIN

```python
# Получить все посты пользователя
async def get_user_posts(user_id: int):
    async with async_session() as session:
        result = await session.execute(select(Post).where(Post.user_id == user_id))
        return result.scalars().all()
```

---

## 📘 Полезные методы выборки

| Что нужно         | Как получить                        |
|------------------|-------------------------------------|
| Все              | `.scalars().all()`                  |
| Первый           | `.scalars().first()`                |
| Один (или None)  | `.scalar_one_or_none()`             |
| Один строго      | `.scalar_one()`                     |
| Много колонок    | `result.all()` → список кортежей    |

---

## 🧠 Пример `to_dict()`

```python
def to_dict(self):
    return {
        "id": self.id,
        "name": self.name,
        "age": self.age
    }
```

---

👨‍💻 Автор шпаргалки: Смитти и ChatGPT
