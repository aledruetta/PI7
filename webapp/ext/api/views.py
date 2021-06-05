from datetime import datetime

from flask_jwt import jwt_required
from flask_restful import Resource

from webapp.ext.api.models import Thing
from webapp.ext.auth import UserAuth
from webapp.ext.db import db

HTTP_RESPONSE_CREATED = 201
HTTP_RESPONSE_NOT_FOUND = 404


class ApiUserAll(Resource):
    @jwt_required()
    def get(self):
        usuarios = UserAuth.query.all()

        return {"usuarios": [user.json() for user in usuarios]}


class ApiUser(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            usuario = UserAuth.query.get(user_id)
            return {"usuario": usuario.json()}

        except AttributeError:
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND


class ApiThingAll(Resource):
    @jwt_required()
    def get(self):
        coisas = Thing.query.all()

        return {"coisas": [coisa.json() for coisa in coisas]}


class ApiThing(Resource):
    @jwt_required()
    def get(self, thing_id):
        try:
            coisa = UserAuth.query.get(thing_id)
            return {"usuario": coisa.json()}

        except AttributeError:
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND
