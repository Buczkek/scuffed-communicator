from sqlalchemy import Column, Integer, String, NUMERIC, create_engine, ForeignKey, Time, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Books(Base):
    __tablename__ = 'Books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    author_id = Column(Integer, ForeignKey('Authors.id'))


class Authors(Base):
    __tablename__ = 'Authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))


class Rentals(Base):
    __tablename__ = 'Rentals'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date())
    book_id = Column(Integer, ForeignKey('Books.id'))


engine = create_engine('sqlite:///biblioteka.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

auths = [Authors(name='a1'),
         Authors(name='a2'),
         Authors(name='a3')
         ]
books = [Books(name="book1", author_id=1),
         Books(name="book2", author_id=1),
         Books(name="book3", author_id=3)
         ]
rent = [Rentals(date=datetime.strptime("01.01.1991", '%d.%m.%Y'), book_id='2')]

for a in auths:
    session.add(a)

for b in books:
    session.add(b)

for r in rent:
    session.add(r)

for row in session.query(Authors).all():
    print(row.id, row.name)

for row in session.query(Books).all():
    print(row.id, row.name, row.author_id)

for row in session.query(Rentals).all():
    print(row.id, row.date, row.book_id)


"""for row in session.query(Books).all():
    print(row.id, row.name, row.author)
"""
"""session.query(Books).filter(Books.id == 2).delete()
session.commit()

for row in session.query(Books).all():
    print(row.id, row.name, row.author)"""
