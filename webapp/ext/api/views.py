import sqlalchemy
from flask import request
from flask_jwt import jwt_required
from flask_restful import Resource
from passlib.hash import pbkdf2_sha512
from validate_email import validate_email

from webapp.ext.api.repository import ThingRepository as thing_repo
from webapp.ext.api.repository import UserRepository as user_repo
from webapp.ext.api.repository import MqttRepository as mqtt_repo

HTTP_RESPONSE_CREATED = 201
HTTP_RESPONSE_BAD_REQUEST = 400
HTTP_RESPONSE_ANAUTHORIZE = 401
HTTP_RESPONSE_NOT_FOUND = 404


class ApiUser(Resource):
    def post(self):
        email = request.json["email"]

        if not validate_email(email, check_smtp=False):
            return {"error": "Email inválido!"}, HTTP_RESPONSE_BAD_REQUEST

        password = request.json["password"]
        hashed_password = pbkdf2_sha512.hash(password)

        try:
            user_repo.save(email, hashed_password)
            mqtt_repo.save(email, password)
        except sqlalchemy.exc.IntegrityError:
            return {"error": "A conta de usuário já existe!"}, HTTP_RESPONSE_BAD_REQUEST

        return {"resposta": "Created!"}, HTTP_RESPONSE_CREATED

    @jwt_required()
    def get(self):
        users = user_repo.get_all()
        return {"usuarios": [user.json() for user in users]}


class ApiUserId(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            user = user_repo.get_by_id(user_id)
            return {"usuario": user.json()}
        except AttributeError:
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND


class ApiThing(Resource):
    @jwt_required()
    def post(self):
        body = request.json
        user = user_repo.get_by_email(body["email"])
        thing_repo.save(body["mac"], user)

        return {"resposta": "Created!"}, HTTP_RESPONSE_CREATED

    @jwt_required()
    def get(self):
        things = thing_repo.get_all()

        return {"coisas": [thing.json() for thing in things]}


class ApiThingId(Resource):
    @jwt_required()
    def get(self, thing_id):
        try:
            thing = thing_repo.get_by_id(thing_id)
            return {"thing": thing.json()}

        except AttributeError:
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND
