from xmlapp_db import Person, Files, Connections
from base import Base
from sqlalchemy import create_engine


#p1 = Person("Israel", "Ceballos", "imceballos@gmail.com", "password1", "spvrigo")
#p1.save()

engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

p4 = Person("Andrei", "Popescu", "andrei@gmail.com", "password4", "", "spvrigo")
#p4.save()

p3 = Person("Jesus", "Martinez", "jesus@gmail.com", "password3", "", "spvrigo")
#p3.save()

p2 = Person("Gonzalo", "Uribe", "gonzalo@gmail.com", "password2", "", "spvrigo")
#p2.save()

p1 = Person("Israel", "Ceballos", "israel@gmail.com", "password1", "", "spvrigo")
#p1.save()

p3 = Person.find_by_email("gonzalo@gmail.com")
print(p3.first_name)
print(p3.last_name)
print(p3.password)

p4 = Person.find_by_first_name("Israel")
print(p4.last_name)

p8=Person("Eren3", "Jeager", "eren3@gmail.com", "password5", "", "spvirgo")
p8.save()

#----------------------------------------------------

c1=Connections("prueba2", "127.0.0.1", "Eren", "pass5", "test", "path")
#c1.save()

c9=Connections("prueba10", "127.0.0.1", "Eren10", "pass13", "test", "path")
#c9.save()

cf=Connections.find_by_connname("prueba")
print(cf.server)

elements = Files.find_all()
for elem in elements:
    print(elem.filename, elem.size, elem.status, elem.assignedto, elem.sent, elem.stage)
