import subprocess
from webapp.ext.db import db
from webapp.ext.api.models import UserAuth


def save_user(email, password, hashed_password):
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
