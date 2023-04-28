from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db = declarative_base()
engine = create_engine("sqlite:///mydb.db")
Session = sessionmaker(bind=engine)
session = Session()

class Base(db):
    __abstract__ = True

    def __init__(self):
        self.session = session

    def __repr__(self):
        mydict = vars(self)
        mydict.pop("_sa_instance_state")
        return mydict

    def save(self):
        try:
            session.add(self)
            session.commit()
            return self
        except Exception as exc:
            print("log exc {}".format(str(exc)))
            return False

    def delete(self):
        try:
            session.delete(self)
            session.commit()
            return True
        except Exception as exc:
            print("log exc {}".format(str(exc)))
            return False

    def update(self, props: dict):
        try:
            for key, value in props.items():
                print("ENTRO ACA AL MENOS O NO")
                print(key, value)
                setattr(self, key, value)

            session.commit()
            session.flush()
            return self
        except Exception as exc:
            print("log exc {}".format(str(exc)))
            return False


#engine = create_engine("sqlite:///mydb.db", echo=True)
#Base.metadata.create_all(bind=engine)

#Session = sessionmaker(bind=engine)
#session = Session()

#person = Person(1, "Israel", "Ceballos", "imceballos@gmail.com")
#session.add(person)
#session.commit()

#print(Person.find_by_email("imceballos@gmail.com"))