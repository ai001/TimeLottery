from flask import render_template, make_response
from flask.ext.mail import Message
from functools import wraps, update_wrapper
from config import ADMINS, AVATAR_ALLOWED_EXTENSIONS, UID_SIZE
from .decorators import async
from app import mail
from datetime import datetime
import time
import random
import string

# This is used to generate random uids for user.
# Same UID is used for payment reference so can't use standard uuid.uuid4() as it generates very long string
def uid_generator(size=UID_SIZE, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Returns current UTC date time
def utc_now():
    return datetime.utcnow()

# Returns current UTC date time
def utc_now_int():
    return int(time.time())


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def user_registered_email(email, uid, verification_code):
    send_email("User registration verification",
               ADMINS[0],
               ['afsar.imam@gmail.com'],
               render_template("email/auth/register.txt",
                               uid=uid, verification_code=verification_code),
               render_template("email/auth/register.html",
                               uid=uid, verification_code=verification_code))


def forgot_password_email(uid, verification_code):
    send_email("Forgot password verification",
               ADMINS[0],
               ['afsar.imam@gmail.com'],
               render_template("email/auth/password_reset.txt",
                               uid=uid, verification_code=verification_code),
               render_template("email/auth/password_reset.html",
                               uid=uid, verification_code=verification_code))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in AVATAR_ALLOWED_EXTENSIONS


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        print(serial)
        return serial
    raise TypeError ("Type not serializable")