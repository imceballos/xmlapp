from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, Enum
from sqlalchemy.orm import sessionmaker, relationship
import uuid
import re

from base import Base

class Person(Base):
    __tablename__ = "person"

    id = Column("id", String(length=80), primary_key=True)
    first_name = Column("first_name", String(length=80), nullable=False)
    last_name = Column("last_name", String(length=80), nullable=False)
    email = Column("email", String(length=60), nullable=False, unique=True)
    password = Column("password", String(length=256), nullable=False)
    company = Column("company", String(length=60), nullable=False)

    def __init__(self,  first_name, last_name, email, password, company):
        self.id = str(uuid.uuid4())
        self.first_name = self._sanitize_input(first_name)
        self.last_name = self._sanitize_input(last_name)
        self.email = self._validate_email(email)
        self.password = password
        self.company = company
        self.session = self._session()

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
        return re.sub(r'[^\w\s]', '', input_str).replace(' ', '_')

    def _validate_email(self, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("El email es inválido")
        return email
    
class Files(Base):
    __tablename__ = 'files'

    uuid = Column("uuid", String(length=80), primary_key=True)
    filename = Column("filename", String(length=80), nullable=False)
    path = Column("path", String(length=80), nullable=False)
    assignedto = Column("assignedto", String, ForeignKey('person.id'))
    status = Column(Enum('accepted', 'rejected', 'pending', name='status'), default='pending')
    stage = Column("stage", String(length=80), nullable=False)

    def __init__(self, filename, path, assignedto, stage):
        self.uuid = str(uuid.uuid4())
        self.filename = filename
        self.path = path
        self.assignedto = assignedto
        self.stage = stage

    def __repr__(self):
        return f"{self.uuid} {self.filename} {self.path} {self.assignedto} {self.status}"  
    
    @classmethod
    def _session(cls):
        engine = create_engine("sqlite:///mydb.db")
        Session = sessionmaker(bind=engine)
        return Session()

    @classmethod
    def find_by_uuid(cls, uuid):
        session = cls._session()
        return session.query(cls).filter_by(uuid=uuid).first()

    @classmethod
    def find_by_filename(cls, filename):
        session = cls._session()
        return session.query(cls).filter_by(filename=filename).first()

    @classmethod
    def find_by_condition(cls, status):
        session = cls._session()
        return session.query(cls).filter_by(status=status).all()
    


#Session = sessionmaker(bind=engine)
#session = Session()

#person = Person("Israel", "Ceballos", "imceballos1@gmail.com", "imceballos", "testing")
#session.add(person)
#session.commit()

#print(Person.find_by_email("imceballos1@gmail.com"))

#faile = Files("Helloxml", "hELLOWORLD.xml", "51534e87-ea89-456a-a42a-5e255a437a62")

#session.add(faile)
#session.commit()

#elem = Files.find_by_condition("pending")
#for el in elem:
#    print(el.uuid, el.status, el.filename)
