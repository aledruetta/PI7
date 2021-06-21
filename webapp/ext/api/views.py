import sqlalchemy
from flask import request
from flask_jwt import jwt_required
from flask_restful import Resource
from marshmallow import Schema, ValidationError, fields, validate
from passlib.hash import pbkdf2_sha512

from webapp.ext.api.repository import MqttRepository as mqtt
from webapp.ext.api.repository import ThingRepository as thing
from webapp.ext.api.repository import UserRepository as user

# HTTP RESPONSE CODES
CREATED = 201
BAD_REQUEST = 400
ANAUTHORIZE = 401
NOT_FOUND = 404

locales = ["pt_BR", "pt"]


class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8, max=30))


class ThingSchema(Schema):
    email = fields.Email(required=True)
    mac = fields.Str(required=True, validate=validate.Length(equal=6))


class ApiUser(Resource):
    def post(self):
        try:
            UserSchema().load(request.json)
        except ValidationError as err:
            return err.messages, BAD_REQUEST

        email = request.json["email"].lower()
        password = request.json["password"]
        hashed_password = pbkdf2_sha512.hash(password)

        try:
            user.save(email, hashed_password)
            mqtt.save_user(email, password)
        except sqlalchemy.exc.IntegrityError:
            return {"error": "A conta de usuário já existe!"}, BAD_REQUEST

        return {"resposta": "Created!"}, CREATED

    @jwt_required()
    def get(self):
        users = user.get_all()
        return {"usuarios": [user.json() for user in users]}


class ApiUserId(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            u = user.get_by_id(user_id)
            return {"usuario": u.json()}
        except AttributeError:
            return {"error": "Recurso inexistente!"}, NOT_FOUND


class ApiThing(Resource):
    @jwt_required()
    def post(self):
        try:
            ThingSchema().load(request.json)
        except ValidationError as err:
            return err.messages, BAD_REQUEST

        mac = request.json["mac"].upper()
        email = request.json["email"].lower()

        try:
            u = user.get_by_email(email)
            thing.save(mac, u)
            mqtt.save_thing(mac, email)
            return {"resposta": "Created!"}, CREATED
        except AttributeError:
            return {"error": "Recurso inexistente!"}, NOT_FOUND

    @jwt_required()
    def get(self):
        things = thing.get_all()

        return {"coisas": [thing.json() for thing in things]}


class ApiThingId(Resource):
    @jwt_required()
    def get(self, thing_id):
        try:
            t = thing.get_by_id(thing_id)
            return {"thing": t.json()}

        except AttributeError:
            return {"error": "Recurso inexistente!"}, NOT_FOUND
