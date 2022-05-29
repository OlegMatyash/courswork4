from flask import request, abort, json, jsonify
from flask_restx import Resource, Namespace
import utils

from implemented import user_service


auth_ns = Namespace('auth')


@auth_ns.route("/register/")
class AuthView(Resource):

    def post(self):
        req_json = request.json
        password = str(req_json.get("password"))
        password_hash = user_service.make_user_password_hash(password)

        user = user_service.create_new_user(email=req_json.get("email"),
                                            password=password_hash)

        return "Регистрация выполнена"


@auth_ns.route("/login/")
class AuthView(Resource):
    def post(self):
        req_json = request.json
        user = user_service.get_by_email(email=req_json.get("email"))
        password = user.password
        new_password = str(req_json.get("password"))
        new_password_hash = user_service.make_user_password_hash(new_password)
        if password == new_password_hash:
            token = user_service.encode_auth_token(user.email, str(user.password))
            access_token = str(token["access_token"])
            refresh_token = str(token["refresh_token"])
            return {"access_token": access_token, "refresh_token": refresh_token}, 201

    def put(self):
        req_json = request.json
        token = req_json.get("refresh_token")

        tokens = user_service.approve_refresh_token(token)

        return json.dumps(tokens), 201
