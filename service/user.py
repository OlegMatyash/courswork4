import base64
import calendar
import datetime
from flask import request, abort, json
from dao.user import UserDAO
import hashlib
import hmac
from constants import secret, algo, PWD_HASH_SALT, PWD_HASH_ITERATIONS
import jwt


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def create_new_user(self, email, password):
        return self.dao.create(email=email, password=password)

    def check_auth(self, email, password):
        return str(hash(self.dao.get_by_email(email=email.password)) == str(hash(password)))

    def get_by_email(self, email):
        return self.dao.get_by_email(email=email)

    def get_by_id(self, id):
        return self.dao.get_by_id(id=id)

    def update(self, data):
        self.dao.update(data)
        return self.dao

    def update_password(self, data):
        self.dao.update_password(data)
        return self.dao

    def make_user_password_hash(self, password):
        return base64.b64encode(hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    def encode_auth_token(self, email, password):
        data = {
            "email": email,
            "password": password
                }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, secret, algorithm=algo)
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, secret, algorithm=algo)
        return {"access_token": access_token, "refresh_token": refresh_token}

    def decode_auth_token(self, auth_token):
        try:
            payload = jwt.decode(auth_token, 'SECRET_KEY')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(refresh_token, secret, algo)
        email = data.get("email")

        return self.encode_auth_token(email, None)

    def compare_passwords(self, password_hash, other_password):
        return hmac.compare_digest(
            base64.b64decode(password_hash),
            hashlib.pbkdf2_hmac('sha256', other_password.encode(), PWD_HASH_SALT, PWD_HASH_ITERATIONS)
        )
