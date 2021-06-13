import subprocess

from webapp.ext.api.models import Thing, UserAuth
from webapp.ext.db import db


class UserRepository:
    @staticmethod
    def get_all():
        return UserAuth.query.all()

    @staticmethod
    def get_by_id(user_id):
        return UserAuth.query.get(user_id)

    @staticmethod
    def get_by_email(email):
        return UserAuth.query.filter_by(email=email).first()

    @staticmethod
    def save(email, hashed_password):
        user = UserAuth(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()


class ThingRepository:
    @staticmethod
    def get_all():
        return Thing.query.all()

    @staticmethod
    def get_by_id(thing_id):
        return Thing.query.get(thing_id)

    @staticmethod
    def save(mac, user):
        thing = Thing(mac=mac, user=user)
        db.session.add(thing)
        db.session.commit()


class MqttRepository:
    def save(email, password):
        cmd_pass = [
            "/usr/bin/sudo",
            "/usr/bin/mosquitto_passwd",
            "-b",
            "/etc/mosquitto/passwd",
            email,
            password,
        ]
        process = subprocess.Popen(cmd_pass, stdout=subprocess.PIPE)
        # output, error = process.communicate()

        cmd_sysd = ["/usr/bin/sudo", "/usr/bin/systemctl", "reload", "mosquitto.service"]
        process = subprocess.Popen(cmd_sysd, stdout=subprocess.PIPE)
        # output, error = process.communicate()
