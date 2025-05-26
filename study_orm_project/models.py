from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Integer, String, Column, Text, ForeignKey, Date

Base = declarative_base()

#
# class Users(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=False)
#     email = Column(String(50), nullable=False, unique=True)
#
#     # user = relationship('Users', back_populates='profile')
#
#
# class Profile(Base):
#     __tablename__ = 'profiles'
#     id = Column(Integer, primary_key=True)
#     bio = Column(Text, nullable=False)
#
#     # user_id = Column('user_id', ForeignKey('users.id'), unique=True)
#     # profile = relationship('Profile', back_populates='user')


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    books = relationship('Book', back_populates='author')


class Book(Base):


    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), unique=True)

    author = relationship('Author', back_populates='books')


class Student(Base):
    __tablename__ = 'students'
    id =  Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age =  Column(Integer, nullable=False)

    courses = relationship('Course', secondary='student_courses', back_populates='students')


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    students = relationship('Student', secondary='student_courses', back_populates='courses')


class StudentCourse(Base):
    __tablename__ = 'student_courses'

    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), primary_key=True)


class UserSubscription(Base):
    __tablename__ = 'user_subscriptions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))
    start_date = Column(Date, nullable=False)

    user = relationship("User", back_populates="subscriptions_assoc")
    subscription = relationship("Subscription", back_populates="users_assoc")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    subscriptions_assoc = relationship("UserSubscription", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", secondary='user_subscriptions', viewonly=True)


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    users_assoc = relationship("UserSubscription", back_populates="subscription", cascade="all, delete-orphan")
    users = relationship("User", secondary='user_subscriptions', viewonly=True)


'''
Дополнительные советы:
Для start_date используйте тип DateTime (если нужна дата и время) или Date (если только дата).

Связь многие-ко-многим организуется через параметр secondary, который указывает на ассоциативную таблицу.

Имена для back_populates должны соответствовать названиям атрибутов в связанных моделях.

Этого достаточно, чтобы начать реализацию без готового решения. 😊
'''