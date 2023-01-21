from sqlalchemy import Column, Integer, String, NUMERIC, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    value = Column(NUMERIC)


engine = create_engine('sqlite:///example.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

newTest = Test(
    id=2,
    name="ORM",
    value=6.8
)

session.add(newTest)

for row in session.query(Test).all():
    print(row.id, row.name, row.value)
