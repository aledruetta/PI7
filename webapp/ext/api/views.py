from datetime import datetime

from flask import request
from flask_jwt import jwt_required
from flask_restful import Resource
from passlib.hash import sha256_crypt

from webapp.ext.api.models import Thing
from webapp.ext.auth import UserAuth
from webapp.ext.db import db

HTTP_RESPONSE_CREATED = 201
HTTP_RESPONSE_NOT_FOUND = 404


class ApiUser(Resource):
    def post(self):
        body = request.json
        password = sha256_crypt.hash(body["password"])
        user = UserAuth(email=body["email"], password=password)
        db.session.add(user)
        db.session.commit()

        return {"response": "Created!"}, HTTP_RESPONSE_CREATED

    @jwt_required()
    def get(self):
        users = UserAuth.query.all()

        return {"usuarios": [user.json() for user in users]}


class ApiUserId(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            user = UserAuth.query.get(user_id)
            return {"usuario": user.json()}

        except AttributeError:
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND


class ApiThing(Resource):
    @jwt_required()
    def post(self):
        body = request.json
        user = UserAuth.query.filter_by(email=body["email"]).first()
        thing = Thing(mac=body["mac"], user=user)
        db.session.add(thing)
        db.session.commit()

        return {"response": "Created!"}, HTTP_RESPONSE_CREATED

    @jwt_required()
    def get(self):
        things = Thing.query.all()

        return {"coisas": [thing.json() for thing in things]}


class ApiThingId(Resource):
    @jwt_required()
    def get(self, thing_id):
        try:
            thing = UserAuth.query.get(thing_id)
            return {"usuario": thing.json()}

        except AttributeError:
            return {"error": "Recurso inexistente!"}, HTTP_RESPONSE_NOT_FOUND
