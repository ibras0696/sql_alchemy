from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from study_orm_project.models import Base

engine = create_engine('sqlite:///../study_orm_project/test.db',
                       echo=False,
                       pool_size=10,
                       max_overflow=5)


SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

session = SessionLocal()

Base.metadata.create_all(engine)
