from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import re

Base = declarative_base()

class Person(Base):
    __tablename__ = "people"

    id = Column("id", Integer, primary_key=True)
    first_name = Column("first_name", String(length=80), nullable=False)
    last_name = Column("last_name", String(length=80), nullable=False)
    email = Column("email", String(length=60), nullable=False, unique=True)
    username = Column("username", String(length=60),nullable=False, unique=True)
    company = Column("company", String(length=60),nullable=False)

    def __init__(self, id, first_name, last_name, email, username, company):
        self.id = id
        self.first_name = self._sanitize_input(first_name)
        self.last_name = self._sanitize_input(last_name)
        self.email = self._validate_email(email)
        self.username = username
        self.company = company

    def __repr__(self):
       return f"{self.id} {self.first_name} {self.last_name} {self.email} {self.company}"

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
    def find_by_first_name(cls, first_name):
        session = cls._session()
        return session.query(cls).filter_by(first_name=first_name).all()
    
    @classmethod
    def find_by_last_name(cls, last_name):
        session = cls._session()
        return session.query(cls).filter_by(last_name=last_name).all()
    
    @classmethod
    def find_by_id(cls, id):
        session = cls._session()
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def find_by_email(cls, email):
        session = cls._session()
        return session.query(cls).filter_by(email=email).first()
    
    #Actualiza
    @classmethod
    def update_by_id(cls, id, update_dict):
        session = cls._session()
        instance = session.query(cls).get(id)
        for key, value in update_dict.items():
            setattr(instance, key, value)
        session.commit()
    
    @classmethod
    def find_by_company(cls, company):
        session = cls._session()
        return session.query(cls).filter_by(company=company).first()

    @classmethod
    def _session(cls):
        engine = create_engine("sqlite:///mydb.db")
        Session = sessionmaker(bind=engine)
        return Session()

    def _sanitize_input(self, input_str):
    # Reemplaza los caracteres no alfanuméricos y los espacios en blanco por guiones bajos
        return re.sub(r'[^\w\s]', '', input_str).replace(' ', '_')

    def _validate_email(self, email):
    # Verifica que el email tenga un formato válido
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("El email es inválido")
        return email
    
# Crear una clase de modelo para la tabla "Files"
class Files(Base):
    __tablename__ = 'Files'

    uvid = Column("uvid", Integer, primary_key=True)
    filename = Column("filename", String)
    path = Column("path", String)
    assignedto = Column("assignedto", String, ForeignKey('people.username'))
    condition = Column("condition", String)

    user = relationship('people', foreign_keys=[assignedto])  

    def __repr__(self):
        return f"{self.uvid} {self.filename} {self.path} {self.assignedto} {self.condition}"  
    
    @classmethod
    def find_by_uvid(cls, uvid):
        session = cls._session()
        return session.query(cls).filter_by(uvid=uvid).first()

    @classmethod
    def find_by_filename(cls, filename):
        session = cls._session()
        return session.query(cls).filter_by(filename=filename).first()

    @classmethod
    def find_by_condition(cls, condition):
        session = cls._session()
        return session.query(cls).filter_by(condition=condition).all()
    
#engine = create_engine("sqlite:///mydb.db", echo=True)
#Base.metadata.create_all(bind=engine)

#Session = sessionmaker(bind=engine)
#session = Session()

#person = Person(1, "Israel", "Ceballos", "imceballos@gmail.com")
#session.add(person)
#session.commit()

#print(Person.find_by_email("imceballos@gmail.com"))