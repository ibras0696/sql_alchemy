from datetime import date

from sqlalchemy.exc import IntegrityError

from study_orm_project.models import User, Author, Book, Subscription, UserSubscription
from study_orm_project.db import session, SessionLocal


# def add_user(name: str, email: str):
#     with SessionLocal() as conn:
#         try:
#             user = Users(name=name, email=email)
#             conn.add(user)
#             conn.commit()
#         except IntegrityError:
#             return 'Такой пользователь уже есть'
#     return f'User created'
#
#
# def get_users():
#     with SessionLocal() as conn:
#         users = conn.query(Users).all()
#         return users
#
#
# def update_name_by_id(id: int, new_email: str):
#     with SessionLocal() as conn:
#         user = conn.query(Users).filter_by(id=id).first()
#         user.email = new_email
#         conn.commit()
#
#
# def add_new_author(name: str):
#     try:
#         with SessionLocal() as conn:
#             author = Author(name=name)
#             conn.add(author)
#             conn.commit()
#     except Exception as ex:
#         return f'Ошибка: {ex}'
#     else:
#         return 'Author add'
#
#
# def add_new_book(title: str, author_id: int):
#     try:
#         with SessionLocal() as conn:
#             book = Book(title=title, author_id=author_id)
#             conn.add(book)
#             conn.commit()
#     except Exception as ex:
#         return f'Ошибка: {ex}'
#     else:
#         return 'Book add'
#
#
# def get_all_authors():
#     try:
#         with SessionLocal() as conn:
#             authors = conn.query(Author).all()
#             dct = {
#                 auth.id: auth.name for auth in authors}
#     except Exception as ex:
#         return f'Ошибка: {ex}'
#     else:
#         return dct
#
#
# def get_all_books():
#     try:
#         with SessionLocal() as conn:
#             books = conn.query(Book).all()
#             dct = {
#                 book.id: {
#                     'title': book.title,
#                     'author_id': book.author_id
#                 } for book in books
#             }
#     except Exception as ex:
#         return f'Ошибка: {ex}'
#     else:
#         return dct

# ✅ Добавить пользователя
def create_user(name: str) -> User:
    with SessionLocal() as conn:
        # 🔍 Проверка на существующего пользователя
        existing_user = conn.query(User).filter_by(name=name).first()
        if existing_user:
            print(f"[i] Пользователь '{name}' уже существует. Возвращаю существующий объект.")
            return existing_user

        # ➕ Создание нового пользователя
        user = User(name=name)
        conn.add(user)
        try:
            conn.commit()
            conn.refresh(user)
            return user
        except IntegrityError:
            conn.rollback()
            print(f"[!] Ошибка при добавлении пользователя '{name}'")
            return existing_user

# ✅ Добавить подписку
def create_subscription(name: str) -> int | None:
    with SessionLocal() as conn:
        existing = conn.query(Subscription).filter_by(name=name).first()
        if existing:
            print(f"[!] Подписка '{name}' уже существует.")
            return existing.id  # или None

        sub = Subscription(name=name)
        conn.add(sub)
        try:
            conn.commit()
            conn.refresh(sub)
            return sub.id
        except IntegrityError:
            conn.rollback()
            print(f"[Ошибка] Не удалось создать подписку '{name}' — уже существует.")
            return None

# ✅ Привязать пользователя к подписке
def subscribe_user(user_id: int, subscription_id: int, start_date: date):
    with SessionLocal() as conn:
        stmt = UserSubscription(
            user_id=user_id,
            subscription_id=subscription_id,
            start_date=start_date
        )
        conn.add(stmt)
        conn.commit()

# ✅ Получить список подписок пользователя
def get_user_subscriptions(user_id: int):
    with SessionLocal() as conn:
        user = conn.query(User).filter(User.id == user_id).first()
        return user.subscriptions if user else []

# ✅ Отменить подписку (удалить связь)
def unsubscribe_user(user_id: int, subscription_id: int):
    with SessionLocal() as conn:

        stmt = conn.query(UserSubscription).filter_by(
            user_id=user_id,
            subscription_id=subscription_id
        ).first()
        if stmt:
            conn.delete(stmt)
            conn.commit()

# ✅ Удалить пользователя
def delete_user(user_id: int):
    with SessionLocal() as conn:
        user = conn.query(User).filter(User.id == user_id).first()
        if user:
            conn.delete(user)
            conn.commit()