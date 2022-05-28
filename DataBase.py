# pydoc3 -w ./
# poprawione z zaleceniami PEP8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys

Base = declarative_base()
engine = create_engine("sqlite:///budzet.db", echo=False) 

# tworzenie bazy danych


class Budzet(Base):
    __tablename__ = "Budzet"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    month = Column(String, nullable=False)
    plan = Column(Integer, nullable=False)
    reality = Column(Integer, nullable=False)

    def __str__(self):
        return f'{self.id},{self.category}, {self.plan}, \
        {self.reality}, {self.month}'


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
sesja = Session()


# Czyszczenie bazy


def clearDb():
    Base.metadata.drop_all(bind=engine)

# Dodawanie nowej kategorii


def addCategory(v1, v2, v3, v4):
    sesja.add(Budzet(category=v1, month=v2, plan=v3, reality=v4))
    sesja.commit()

# Wypisywanie zawartosci bazy glownie do testow


def writeBudzet():
    budzets = sesja.query(Budzet).all()
    for budzet in budzets:
        print(budzet)


# Dodawanie kolejnego wydatku do bazy danych
    
def changeCategory(v1, v2, v3):
    sesja.query(Budzet).filter(Budzet.category == v1,
                               Budzet.month == v2).update({'reality': 
                                                           Budzet.reality+v3})
    sesja.commit()
    