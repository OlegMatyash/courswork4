from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from implemented import movie_service
from utils import auth_required

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):

    @auth_required
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        paginator = request.args.get("page")
        status = request.args.get("status")

        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
            "status": status,
        }
        all_movies = movie_service.get_all(filters)
        all_movies = all_movies[:paginator] if paginator else all_movies
        res = MovieSchema(many=True).dump(all_movies)
        return res, 200

    @auth_required
    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    @auth_required
    def get(self, bid):
        b = movie_service.get_one(bid)
        sm_d = MovieSchema().dump(b)
        return sm_d, 200

    @auth_required
    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        movie_service.update(req_json)
        return "", 204

    @auth_required
    def delete(self, bid):
        movie_service.delete(bid)
        return "", 204
