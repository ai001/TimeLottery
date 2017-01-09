import uuid

from flask import Blueprint, request, jsonify, g
from flask.ext.httpauth import HTTPBasicAuth

from app.auth.models import User
from app.utilities.common import utc_now as now, user_registered_email, forgot_password_email

auth_api = Blueprint('auth_api', __name__, url_prefix='/backend/auth/api/v1')
auth = HTTPBasicAuth()


@auth_api.route('/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.email})


@auth_api.route('/make_user', methods=['POST'])
@auth.login_required
def make_user():
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        response = jsonify({'status': 'Fail', 'message': 'Missing parameters'})
        response.status_code = 400
        return response

    if User.objects.filter(email=email).first() is not None:
        response = jsonify({'status': 'Fail', 'message': 'User already exists'})
        response.status_code = 400
        return response

    user = User(email=email)
    user.hash_password(password)
    user.activity.created = now()
    verification_code = uuid.uuid4()
    user.activity.verification_code = str(verification_code)
    user.save()

    user_registered_email(email, verification_code)

    response = jsonify({'status': 'Success', 'message': 'User created'})
    response.status_code = 201
    return response


@auth_api.route('/login', methods=['GET'])
def login():
    email = request.authorization.username
    password = request.authorization.password
    print(email, password)
    if email is None or password is None:
        response = jsonify({'status': 'Fail', 'message': 'Missing parameters'})
        response.status_code = 400
        return response

    user = User.objects.filter(email=email).first()
    if not user or not user.verify_password(password):
        user = None
        response = jsonify({'status': 'Fail', 'message': 'Authentication failure'})
        response.status_code = 403
        return response
    else:
        g.user = user
        token = g.user.generate_auth_token(600)

        user.activity.valid_tokens.append(user.hash_token(token.decode('ascii')))
        user.save()

        response = jsonify(
            {'status': 'Success', 'message': 'User logged-in', 'token': token.decode('ascii'), 'duration': 600})
        response.status_code = 200
        return response


@auth_api.route('/renew_token', methods=['GET'])
@auth.login_required
def get_auth_token():
    old_token = request.authorization.username
    new_token = g.user.generate_auth_token(600)
    g.user.remove_token(old_token)
    g.user.activity.valid_tokens.append(g.user.hash_token(new_token.decode('ascii')))
    g.user.save()

    response = jsonify(
        {'status': 'Success', 'message': 'Token renewed', 'token': new_token.decode('ascii'), 'duration': 600})
    response.status_code = 200
    return response


@auth_api.route('/logout', methods=['GET'])
@auth.login_required
def remove_token():
    token = request.authorization.username
    g.user.remove_token(token)
    g.user.save()

    response = jsonify({'status': 'Success', 'message': 'User logged out'})
    response.status_code = 200
    return response


@auth_api.route('/details', methods=['GET'])
@auth.login_required
def get_user():
    # user = User.objects(pk=id).first()
    # if not user or user.email != g.user.email:
    #    response = jsonify({'status': 'Fail', 'message': 'Invalid data'})
    #    response.status_code = 404
    #    return response
    return jsonify({'status': 'Success', 'message': 'User logged-in', 'user_profile': g.user.profile})



# User will only be verified by token, so a token must be obtained by login first
@auth.verify_password
def verify_password(token, ignore):
    # Try to authenticate by token
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True

