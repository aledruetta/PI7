from datetime import datetime
from passlib.hash import sha256_crypt

from flask import request
from flask_jwt import jwt_required
from flask_restful import Resource

from webapp.ext.api.models import Thing
from webapp.ext.auth import UserAuth
from webapp.ext.db import db

HTTP_RESPONSE_CREATED = 201
HTTP_RESPONSE_NOT_FOUND = 404


class ApiUser(Resource):
    def post(serf):
        body = request.get_json()
        password = sha256_crypt.hash(body.password)
        user = UserAuth(email=body.email, password=password)
        db.session.add(user)
        db.session.commit()

        return HTTP_RESPONSE_CREATED

    @jwt_required()
    def get(self):
        usuarios = UserAuth.query.all()

        return {"usuarios": [user.json() for user in usuarios]}


class ApiUserId(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            usuario = UserAuth.query.get(user_id)
            return {"usuario": usuario.json()}

        except AttributeError:
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND


class ApiThing(Resource):
    @jwt_required()
    def get(self):
        coisas = Thing.query.all()

        return {"coisas": [coisa.json() for coisa in coisas]}


class ApiThingId(Resource):
    @jwt_required()
    def get(self, thing_id):
        try:
            coisa = UserAuth.query.get(thing_id)
            return {"usuario": coisa.json()}

        except AttributeError:
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND
