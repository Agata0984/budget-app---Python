# pydoc3 -w ./
# poprawione z zaleceniami PEP8

import pytest
import factory
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine("sqlite:///test.db", echo=False)


@pytest.fixture(scope='module')
def connection():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='function')
def session(connection):
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()


class Budzet:
    def __init__(self, mon, cat, p, r):
        self.category = cat
        self.month = mon
        self.plan = p
        self.reality = r


class BudzetFactory(factory.Factory):
    category = factory.Faker('category')
    month = factory.Faker('month')
    plan = factory.Faker('plan')
    reality = factory.Faker('reality')

    class Meta:
        model = Budzet


class BudzetModel(Base):
    __tablename__ = "BudzetModel"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    month = Column(String, nullable=False)
    plan = Column(Integer, nullable=False)
    reality = Column(Integer, nullable=False)


class BudzetFactory(factory.alchemy.SQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: '%s' % n)
    category = factory.Faker('category')
    month = factory.Faker('month')
    plan = factory.Faker('plan')
    reality = factory.Faker('reality')

    class Meta:
        model = BudzetModel

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
sesja = Session()

pytest.fixture(scope='function')


def session(connection):
    transaction = connection.begin()
    session = Session(bind=connection)
    BudzetFactory._meta.sqlalchemy_session = session
    yield session
    session.close()
    transaction.rollback()
    
# Sprawdzenie dzialania fukcji dodajacej nowa kategotrie do bazy


def add_category(v1, v2, v3, v4):
    sesja.add(BudzetModel(category=v1, month=v2, plan=v3, reality=v4))
    sesja.commit()


def test_case():
    add_category("ubrania", "luty", 100, 20)
    result = sesja.query(BudzetModel).first()
    assert result.category == "ubrania"
    assert result.month == "luty"
    assert result.plan == 100
    assert result.reality == 20

# Sprawdzenie dzialania fukcji aktualizujacej wydatki


def change_category(v1, v2, v3):
    sesja.query(BudzetModel).filter(BudzetModel.category == v1,
                                    BudzetModel.month == v2).update({'reality': 
                                                                    BudzetModel
                                                                    .reality+v3
                                                                     })
    sesja.commit()


def test_case2():
    change_category("ubrania", "luty", 13)
    result = sesja.query(BudzetModel).filter(BudzetModel.category == "ubrania",
                                             BudzetModel.month == "luty"
                                             ).first()
    assert result.reality == 33

test_case()
test_case2()
