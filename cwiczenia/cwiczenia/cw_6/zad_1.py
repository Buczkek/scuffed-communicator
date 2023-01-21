from sqlalchemy import Column, Integer, String, NUMERIC, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Books(Base):
    __tablename__ = 'Books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    author = Column(String(100))


engine = create_engine('sqlite:///biblioteka.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

B = Books(
    id=2,
    name="book1",
    author="auth1"

)

# session.add(B)
session.commit()

for row in session.query(Books).all():
    print(row.id, row.name, row.author)

session.query(Books).filter(Books.id == 2).delete()
session.commit()

for row in session.query(Books).all():
    print(row.id, row.name, row.author)
