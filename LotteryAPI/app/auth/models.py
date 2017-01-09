# Import the database object (db) from the main application module
from app import db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
#from PIL import Image
from app.utilities.common import utc_now as now, uid_generator
from config import SECRET_KEY, UID_SIZE


class PasswordReset(db.EmbeddedDocument):
    requested_at = db.DateTimeField()
    verification_code = db.UUIDField(binary=True)
    changed_at = db.DateTimeField()

class EmailVerification(db.EmbeddedDocument):
    email_verified = db.DateTimeField()
    verification_code = db.UUIDField(binary=True)

class ActivityAudit(db.Document):
    uid     = db.StringField(min_length=UID_SIZE, max_length=UID_SIZE)
    created = db.DateTimeField()
    type    = db.StringField(min_length=3, max_length=5)
    code    = db.StringField(required=True)
    headers = db.DictField()
    text    = db.StringField()

    meta = {
        'indexes': ['uid'],
        'ordering': ['-created']
    }

class UserActivity(db.EmbeddedDocument):
    created             = db.DateTimeField(default=lambda: now())
    email_verification  = db.EmbeddedDocumentField(EmailVerification, default=EmailVerification)
    password_reset      = db.EmbeddedDocumentField(PasswordReset, default=PasswordReset)
    user_restricted     = db.BooleanField(default=False)
    failed_logins       = db.IntField(default=0)
    user_banned         = db.BooleanField(default=False)
    valid_tokens        = db.ListField()
    payment_reference   = db.StringField(min_length=UID_SIZE, max_length=UID_SIZE, unique=True)
    activity_audit      = db.ListField(db.ReferenceField(ActivityAudit))

class Address(db.EmbeddedDocument):
    created         = db.DateTimeField(default=lambda: now())
    address_type    = db.StringField()
    door_no_name    = db.StringField()
    street          = db.StringField()
    line_2          = db.StringField()
    city            = db.StringField()
    county          = db.StringField()
    postcode        = db.StringField(min_length=6, max_length=8)
    country         = db.StringField()

class Plan(db.EmbeddedDocument):
    joined = db.DateTimeField()
    name = db.StringField()
    frequency = db.IntField()

class Payment(db.EmbeddedDocument):
    payment_date = db.DateTimeField()
    amount = db.IntField()

class Default(db.EmbeddedDocument):
    type = db.StringField()
    amount = db.IntField()
    reason = db.StringField()

class Record(db.EmbeddedDocument):
    defaults = db.EmbeddedDocumentField(Default)
    all_due_clear = db.BooleanField()
    lottery_ready = db.BooleanField()
    include_in_lottery = db.BooleanField()

class Billing(db.Document):
    uid = db.StringField(min_length=UID_SIZE, max_length=UID_SIZE, unique=True, required=True)
    plans = db.EmbeddedDocumentField(Plan)
    payments = db.EmbeddedDocumentListField(Payment)
    record = db.EmbeddedDocumentListField(Record)

    meta = {
        'indexes': ['uid'],
    }

class UserProfile(db.EmbeddedDocument):
    updated         = db.IntField(default=0)
    first_name      = db.StringField(max_length=50)
    last_name       = db.StringField(max_length=50)
    public_name     = db.StringField(max_length=50)
    gender          = db.StringField(max_length=1)
    currency        = db.StringField(min_length=3, max_length=3)
    timezone        = db.StringField(min_length=3, max_length=3)
    date_of_birth   = db.DateTimeField()
    avatar          = db.ImageField(size=(300, 300, True))
    interests       = db.ListField()
    addresses       = db.EmbeddedDocumentListField(Address)
    billing         = db.ReferenceField(Billing)



class UserAuthorization(db.EmbeddedDocument):
    roles = db.ListField(default=["norm"])
    groups = db.ListField(default=[])


class User(db.Document):
    uid = db.StringField(required=True, unique=True, default=lambda: uid_generator())
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    authorization = db.EmbeddedDocumentField(UserAuthorization, default=UserAuthorization)
    profile = db.EmbeddedDocumentField(UserProfile, default=UserProfile)
    activity = db.EmbeddedDocumentField(UserActivity, default=UserActivity)

    meta = {
        'indexes': ['email', 'uid'],
        'ordering': ['-activity.created']
    }

    def hash_token(self, token):
        return pwd_context.encrypt(token)

    def verify_token(self, token):
        for db_token in self.activity.valid_tokens:
            if (pwd_context.verify(token, db_token)):
                return True
        return False

    def remove_token(self, token):
        for db_token in self.activity.valid_tokens:
            if (pwd_context.verify(token, db_token)):
                self.activity.valid_tokens.remove(db_token)
                return True
        return False

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        # s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        s = Serializer(SECRET_KEY, expires_in=expiration)
        return s.dumps({'uid': str(self.uid)})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token

        user = User.objects.filter(uid=data['uid']).first()
        return user

