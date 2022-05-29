from dao.model.user import User
from flask import request, abort, json


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def get_by_id(self, id):
        return self.session.query(User).filter(User.id == id).first()

    def create(self, **kwargs):
        ent = User(**kwargs)
        self.session.add(ent)
        self.session.commit()
        return ent

    def update(self, data):
        user = self.get_by_email(data.get("email"))
        user.name = data.get("name")
        user.surname = data.get("surname")
        user.favorite_genre = data.get("favorite_genre")

        self.session.add(user)
        self.session.commit()

    def update_password(self, data):
        user = self.get_by_email(data.get("email"))
        user.password = data.get("password")

        self.session.add(user)
        self.session.commit()
