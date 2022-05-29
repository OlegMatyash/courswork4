from flask import request, json, jsonify
from flask_restx import Resource, Namespace
from dao.model.user import UserSchema
from implemented import user_service
from utils import auth_required

user_ns = Namespace("user")


@user_ns.route("/")
class UserView(Resource):

    @auth_required
    def get(self):
        data = request.json
        email = data["email"]
        user_by_email = user_service.get_by_email(email)
        sm_d = UserSchema().dump(user_by_email)
        return sm_d, 200


    @auth_required
    def patch(self):
        data = request.json
        user_service.update(data)
        email = data["email"]
        user = user_service.get_by_email(email)
        name = str(user.name),
        surname = str(user.surname),
        favorite_genre = str(user.favorite_genre)
        return {"name": name, "surname": surname,
                "favorite_genre": favorite_genre}, 201

    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}


@user_ns.route("/password/")
class UserView(Resource):

    @auth_required
    def put(self):
        req_json = request.json
        other_password = str(req_json.get("password1"))
        password2 = str(req_json.get("password2"))
        password2_hash = user_service.make_user_password_hash(password2)
        user = user_service.get_by_email(email=req_json["email"])
        password_hash = user.password
        result = user_service.compare_passwords(password_hash, other_password)
        if result:
            data = {
                "email": req_json["email"],
                "password": password2_hash,
            }
            user_service.update_password(data)
            return "", 204


@user_ns.route("/<int:uid>")
class UserView(Resource):
    def get(self, uid):
        r = user_service.get_one(uid)
        sm_d = UserSchema().dump(r)
        return sm_d, 200

    def put(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user_service.update(req_json)
        return "", 204

    def delete(self, bid):
        user_service.delete(bid)
        return "", 204