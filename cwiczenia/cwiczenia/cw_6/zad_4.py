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


class Bilioteka():
    def __init__(self, ses):
        self.session = ses

    def add_book(self, name: str, author_id: int):
        self.session.add(Books(name=name, author_id=author_id))
        self.session.commit()

    def del_book(self, book_id: int):
        self.session.query(Books).filter(Books.id == book_id).delete()
        self.session.commit()

    def show_book(self):
        for row in self.session.query(Books).all():
            print(row.id, row.name, row.author_id)

    def add_author(self, name):
        self.session.add(Authors(name=name))
        self.session.commit()

    def del_author(self, author_id: int):
        self.session.query(Books).filter(Books.id == author_id).delete()
        self.session.commit()

    def show_author(self):
        for row in self.session.query(Authors).all():
            print(row.id, row.name)

    def rent_book(self, book_id:int):
        self.session.add(Rentals(date=datetime.now()))
        self.session.commit()



engine = create_engine('sqlite:///biblioteka.db', echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

b = Bilioteka(session)

while True:
    print("1 add book,\n2 add author,\n3 rent book,\n4 del_book,\n 5 del_author")
    command = int(input("1 - 5: "))
    if command == 1:
        name, aut_id = input("book name author_id : ").split()
        b.add_book(name, aut_id)
    if command == 2:
        name = input("author name : ")
        b.add_author(name)
    if command == 3:
        id = input("book_id: ")
        b.rent_book(id)
    if command == 4:
        id = input("book_id: ")
        b.del_book(id)
    if command == 5:
        id = input("author_id: ")
        b.del_author(id)
    print("====BAZA====")
    b.show_book()
    b.show_author()
    print("====END====")