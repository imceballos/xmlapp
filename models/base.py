from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

db = declarative_base()

class Base(db):
    __abstract__ = True

    def __init__(self):
        self.session = self._session()

    def __repr__(self):
        mydict = vars(self)
        mydict.pop("_sa_instance_state")
        return mydict

    def save(self):
        try:
            self.session.add(self)
            self.session.commit()
            return self
        except Exception as exc:
            print("log exc {}".format(str(exc)))
            return False

    def delete(self):
        try:
            self.session.delete(self)
            self.session.commit()
            return True
        except Exception as exc:
            print("log exc {}".format(str(exc)))
            return False

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

#print(Person.find_by_email("imceballos@gmail.com"))