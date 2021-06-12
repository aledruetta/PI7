import subprocess

import sqlalchemy
from flask import request
from flask_jwt import jwt_required
from flask_restful import Resource
from passlib.hash import pbkdf2_sha512
from validate_email import validate_email

from webapp.ext.api.models import Thing, UserAuth
from webapp.ext.db import db

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
            user = UserAuth(email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()

            cmd_pass = [
                "/usr/bin/sudo",
                "/usr/bin/mosquitto_passwd",
                "-b",
                "/etc/mosquitto/passwd",
                user.email,
                password,
            ]
            process = subprocess.Popen(cmd_pass, stdout=subprocess.PIPE)
            output, error = process.communicate()

            cmd_sysd = ["/usr/bin/sudo", "/usr/bin/systemctl", "reload", "mosquitto.service"]
            process = subprocess.Popen(cmd_sysd, stdout=subprocess.PIPE)
            output, error = process.communicate()

        except sqlalchemy.exc.IntegrityError:
            return {"error": "A conta de usuário já existe!"}, HTTP_RESPONSE_BAD_REQUEST

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
