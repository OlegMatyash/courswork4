import jwt
import datetime
from flask import request, abort
from dao.model.user import User
from setup_db import db
from constants import secret


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, secret, algorithms=['HS256'])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def create_new_user(**kwargs):
    ent = User(**kwargs)
    with db.session.begin():
        db.session.add_all([ent])

    return ent


def encode_auth_token(user_id):
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=30),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id
        }
        payload2 = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id
        }
        return {"access_token":
                    jwt.encode(
                        payload,
                        "SECRET_KEY",
                        algorithm="HS256").decode(),
                "refresh_token":
                    jwt.encode(
                        payload2,
                        "SECRET_KEY",
                        algorithm="HS256").decode()
                }

    except Exception as e:
        return e
