from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Person(Base):
    __tablename__ = "people"

    id = Column("id", Integer, primary_key=True)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    email = Column("email", String)

    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
       return f"{self.id} {self.first_name} {self.last_name} {self.email}"

    @classmethod
    def find_by_email(cls, email):
        session = cls._session()
        return session.query(cls).filter_by(email=email).first()

    @classmethod
    def find_by_public_id(cls, public_id):
        session = cls._session()
        return session.query(cls).filter_by(public_id=public_id).first()

    @classmethod
    #Definir classmethods para: Buscar por first_name, last_name, por id, por email
    #Agregar atributo company al tablero users, agregar un classmethod para company
    #Agregar verificadores de email, de caracteres sanitizados y setear un largo maximo de VARCHAR(60-80) 
    #Files: uuid, filename, path, condition
    #Crear metodos de clase para filename, path, contenido dentro de, condition.

    @classmethod
    def _session(cls):
        engine = create_engine("sqlite:///mydb.db")
        Session = sessionmaker(bind=engine)
        return Session()

#engine = create_engine("sqlite:///mydb.db", echo=True)
#Base.metadata.create_all(bind=engine)

#Session = sessionmaker(bind=engine)
#session = Session()

#person = Person(1, "Israel", "Ceballos", "imceballos@gmail.com")
#session.add(person)
#session.commit()

print(Person.find_by_email("imceballos@gmail.com"))