__author__ = 'Bolero'

from app import db
from app.models import Ftasks
from datetime import date

db.create_all()

db.session.add(Ftasks("Finish this tutorial", date(2013, 10, 15), 10, 1))
db.session.add(Ftasks("Finish this book", date(2013, 11, 15), 10, 1))

db.session.commit()

