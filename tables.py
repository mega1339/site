from db_setup import db
from app_setup import app

class User(db.Model):
    id                 = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email              = db.Column(db.String(), unique=True)
    login              = db.Column(db.String(), unique=True)
    password           = db.Column(db.String(), unique=False)

    @staticmethod
    def add(email, login, password):
        with app.app_context():
            db.create_all()
            user = User(email = email,
                        login = login,
                        password = password,
                        )
            db.session.add(user)
            db.session.commit()


class Card(db.Model):
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type        = db.Column(db.String(), unique=False)
    name        = db.Column(db.String(), unique=False)
    description = db.Column(db.String(), unique=False)
    manufactor  = db.Column(db.String(), unique=False)
    price       = db.Column(db.Integer,  unique=False)
    photo       = db.Column(db.String(), unique=False)
    comments    = db.Column(db.String(), unique=False)
    marks       = db.Column(db.String(), unique=False)


    @staticmethod
    def add(type, name, description, manufactor, price, photo):
        with app.app_context():
            db.create_all()
            card = Card(type = type,
                        name = name,
                        description = description,
                        manufactor = manufactor,
                        price = price,
                        photo = photo,
                        comments = '',
                        marks = ''
                       )
            db.session.add(card)
            db.session.commit()