from flask import Flask, Blueprint
from flask_restful import Api, Resource, reqparse, url_for
import json
import datetime
from app.auth.models import User

from app.utilities.common import json_serial

admin_api = Blueprint('admin_api', __name__, url_prefix='/backend/admin/api/v1')

adm_api = Api(admin_api)


class UsersAdministration(Resource):
    def get(self):
        """
        Lists all the users and user's basic data
        """
        data = []

        for user in User.objects:
            data.append({
                "created": user.pk.generation_time.timestamp(),
                "uid": user.uid,
                "email": user.email,
                "first_name": user.profile.first_name if user.profile.first_name else '',
                "last_name": user.profile.last_name if user.profile.last_name else '',
                "email_verified": format(user.activity.email_verification.email_verified),
                "user_restricted": user.activity.user_restricted,
                "failed_logins": user.activity.failed_logins,
                "user_banned": user.activity.user_banned
            })
        
        status = { 'success': True, 'result_length': len(data)}
        response = {'data': data, 'status': status}
        return response

class UserAdministration_Profile(Resource):
    def post(self):
        """
        Lists an individual user's basic data
        """
        data = {}
        email_verified = False
        first_name = ''
        last_name = ''
        gender = ''
        date_of_birth = ''
        
        parser = reqparse.RequestParser()
        parser.add_argument('uid', type=str, location='json', required=True, help='UID for the user to retrieve')
        args = parser.parse_args()

        user = User.objects.filter(uid=args["uid"]).first()
        if user is not None:
            data["created"] = user.pk.generation_time.timestamp()
            data["email"] = user.email
            data["first_name"] = user.profile.first_name
            data["last_name"] = user.profile.last_name
            data["last_name"] = user.profile.last_name
            data["gender"] = user.profile.gender
            data["address"] = {}
            data["address"]["door_no_name"] = user.profile.addresses[0].door_no_name
            data["address"]["street"] = user.profile.addresses[0].street
            data["address"]["line_2"] = user.profile.addresses[0].line_2
            data["address"]["city"] = user.profile.addresses[0].city
            data["address"]["couty"] = user.profile.addresses[0].county
            data["address"]["postcode"] = user.profile.addresses[0].postcode
            data["address"]["country"] = user.profile.addresses[0].country
            data["date_of_birth"] = format(user.profile.date_of_birth) 
            data["email_verified"] = format(user.activity.email_verification.email_verified)
            data["user_restricted"] = user.activity.user_restricted
            data["failed_logins"] = user.activity.failed_logins
            data["user_banned"] = user.activity.user_banned
        
        if user is not None:
            status = { 'success': True, 'result_length': 1 }
        else:
            status = { 'success': False, 'result_length': 0 }
        
        response = {'data': data, 'status': status}
        return response

adm_api.add_resource(UsersAdministration, '/userAdministration/getUsers')
adm_api.add_resource(UserAdministration_Profile, '/userAdministration/getUserProfile')