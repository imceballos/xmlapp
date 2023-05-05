from xmlapp_db import Person, Files
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

p3 = Person.find_by_email("jesus@gmail.com")
p3.update
print(p3.first_name)
print(p3.last_name)
print(p3.password)

elements = Files.find_all()
for elem in elements:
    print(elem.filename, elem.size, elem.status, elem.assignedto, elem.sent, elem.stage)
