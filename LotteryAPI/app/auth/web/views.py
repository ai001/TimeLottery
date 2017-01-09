from app.auth.models import User, UserProfile, ActivityAudit, EmailVerification, Address
from app import cache
from flask import Blueprint, abort, request, jsonify, g, render_template, session, url_for, redirect, make_response, send_file
from werkzeug.utils import secure_filename
from io import BytesIO
from functools import wraps

import uuid
import os, sys

from app.auth.web.forms import RegisterForm, LoginForm, ForgotForm, PasswordResetForm, ProfileForm, AvatarForm
from app.utilities.common import nocache, utc_now, utc_now_int, user_registered_email, forgot_password_email, allowed_file

from pprint import pprint

auth_web = Blueprint('auth_web', __name__, url_prefix='/backend/auth/web', static_folder='../../static')

#cache = Cache(config= { 'CACHE_TYPE' : 'simple'})

## Unbuffered IO for logging, remove after debug
#sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

# Login Decorator
def logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('uid') is not None:
            return f(*args, **kwargs)
        else:
            session['next'] = request.url
            return redirect(url_for('auth_web.login'))
    return decorated_function

def logout_session_clear():
        session.pop('uid', None)
        session.pop('email', None)
        session.pop('first_name', None)
    
@auth_web.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        logout_session_clear()    
        user = User(email=form.email.data)

        user.hash_password(form.password.data)
        user.activity.created = utc_now()
        verification_code = uuid.uuid4()

        user.activity.payment_reference=user.uid

        user.activity.email_verification = EmailVerification(verification_code = str(verification_code))
        user.activity.activity_audit.append(
            ActivityAudit(uid=user.uid, created=utc_now(), code="USER CREATED",
                          text="User created",
                          headers= { "REMOTE_ADDR": request.environ["REMOTE_ADDR"],
                                     "HTTP_USER_AGENT": request.environ["HTTP_USER_AGENT"],
                                     "REMOTE_PORT": request.environ["REMOTE_PORT"],}).save())

        user.save()

        user_registered_email(user.email, user.uid, verification_code)

        return render_template('auth/user_registered.html')
    return render_template('auth/register.html', form=form)

@auth_web.route('/confirm/<uid>/<verification_code>', methods=('GET', 'POST'))
def registration_confirm(uid, verification_code):
    user = User.objects.filter(uid=uid).first()
    if user and user.activity and \
            user.activity.email_verification and \
            user.activity.email_verification.email_verified == None:
        if verification_code == str(user.activity.email_verification.verification_code):
            user.activity.email_verification.email_verified = utc_now()
            user.activity.activity_audit.append(
                ActivityAudit(uid=user.uid, created=utc_now(), type='INFO', code="01002 - EMAIL CONFIRM",
                              text="Email verified",
                              headers={"REMOTE_ADDR": request.environ["REMOTE_ADDR"],
                                       "HTTP_USER_AGENT": request.environ["HTTP_USER_AGENT"],
                                       "REMOTE_PORT": request.environ["REMOTE_PORT"], }).save())

            user.save()
            return render_template('auth/email_confirmed.html')
    else:
        abort(401)


@auth_web.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None

    if request.method == 'POST':
        # set the login form email default if user ticked remember me
        if form.remember_me.data == True:
            session['form_email'] = form.email.data
        else:
            # and remove if he unticked remember me
            session.pop('form_email', None)

    if request.method == 'GET' and request.args.get('next'):
            session['next'] = request.args.get('next')

    if form.validate_on_submit():
        next = session.get('next')
        #session.pop('uid', none)
        user = User.objects.filter(email=form.email.data).first()

        if user:
            if user.activity.user_restricted == False:
                if user.verify_password(form.password.data):
                    if user.activity.email_verification.email_verified and user.activity.email_verification.email_verified < utc_now():
                        user.activity.failed_logins = 0
                        user.activity.activity_audit.append(
                            ActivityAudit(uid=user.uid, created=utc_now(), type='INFO', code="01003 - USER LOGON",
                                          text="User logged in",
                                          headers={"REMOTE_ADDR": request.environ["REMOTE_ADDR"],
                                                   "HTTP_USER_AGENT": request.environ["HTTP_USER_AGENT"],
                                                   "REMOTE_PORT": request.environ["REMOTE_PORT"] }).save())
                        user.save()
                        session['uid']   = user.uid
                        session['email'] = user.email
                        session['updated'] = user.profile.updated
                        # First check if user profile is populated, if not prompt them to complete it first

                        if (user.profile and user.profile.first_name
                                         and user.profile.date_of_birth
                                         and user.profile.addresses):
                            session['first_name'] = user.profile.first_name
                            if next:
                                return redirect(next)
                            else:
                                return redirect(url_for('auth_web.home'))
                        else:
                            # User profile is not populated, send user to profile page
                            return redirect(url_for('auth_web.profile', updated=session.get('updated')))
                    else:
                        user.activity.activity_audit.append(
                            ActivityAudit(uid=user.uid, created=utc_now(), type='WARN', code="11003 - EMAIL NOT CONFIRM",
                                          text="Login succeed but email not verified",
                                          headers={"REMOTE_ADDR": request.environ["REMOTE_ADDR"],
                                                   "HTTP_USER_AGENT": request.environ["HTTP_USER_AGENT"],
                                                   "REMOTE_PORT": request.environ["REMOTE_PORT"] }).save())
                        error = 'Email not verified'
                        user.save()
                        user = None
                else:
                    user.activity.activity_audit.append(
                        ActivityAudit(uid=user.uid, created=utc_now(), type='ERROR', code="11003 - LOGIN FAILURE",
                                      text="Login failed",
                                      headers={"REMOTE_ADDR": request.environ["REMOTE_ADDR"],
                                               "HTTP_USER_AGENT": request.environ["HTTP_USER_AGENT"],
                                               "REMOTE_PORT": request.environ["REMOTE_PORT"] }).save())

                    error = 'Incorrect credentials'
                    user.activity.failed_logins += 1
                    if user.activity.failed_logins > 5:
                        # Too many wrong password attempts, restrict login, resetting password will remove this restriction
                        user.activity.user_restricted = True
                        error = "Too many failed attempts, account locked, please reset password"
                    user.save()
                    user = None
            else:
                user.activity.activity_audit.append(
                    ActivityAudit(uid=user.uid, created=utc_now(), type='WARN', code="11003 - ACCOUNT LOCKED",
                                  text="Account locked",
                                  headers={"REMOTE_ADDR": request.environ["REMOTE_ADDR"],
                                           "HTTP_USER_AGENT": request.environ["HTTP_USER_AGENT"],
                                           "REMOTE_PORT": request.environ["REMOTE_PORT"] }).save())
                error = 'Account locked, please reset password'
                user.save()
                user = None
        else:
            error = 'Incorrect credentials'
    return render_template('auth/login.html', form=form, error=error)


@auth_web.route('/logout')
def logout():
    logout_session_clear() 
    return redirect(url_for('auth_web.login'))


@auth_web.route('/forgot', methods=('GET', 'POST'))
def forgot():
    form = ForgotForm()
    if form.validate_on_submit():
        user = User.objects.filter(email=form.email.data.lower()).first()
        if user:
            verification_code = str(uuid.uuid4())
            user.activity.password_reset.requested_at = utc_now()
            user.activity.password_reset.verification_code = verification_code
            user.activity.activity_audit.append(
                ActivityAudit(uid=user.uid, created=utc_now(), type='INFO', code="01004 - PASSWORD RESET REQUESTED",
                              text="Password reset requested",
                              headers={"REMOTE_ADDR": request.environ["REMOTE_ADDR"],
                                       "HTTP_USER_AGENT": request.environ["HTTP_USER_AGENT"],
                                       "REMOTE_PORT": request.environ["REMOTE_PORT"], }).save())
            user.save()

            # email the user
            forgot_password_email(user.uid, verification_code)

        return render_template('auth/password_forgot_confirmed.html')
    return render_template('auth/forgot.html', form=form)


@auth_web.route('/password_reset/<uid>/<verification_code>', methods=('GET', 'POST'))
def password_reset(uid, verification_code):
    message = None
    require_current = None

    form = PasswordResetForm()

    user = User.objects.filter(uid=uid).first()
    if not user and verification_code != user.activity.password_reset.verification_code:
        abort(401)

    if request.method == 'POST':
        del form.current_password
        if form.validate_on_submit():
            user.hash_password(form.password.data)
            user.activity.password_reset.changed_at = utc_now()
            user.activity.user_restricted = False
            user.activity.failed_logins = 0
            user.activity.activity_audit.append(
                ActivityAudit(uid=user.uid, created=utc_now(), type='INFO', code="01004 - FORGOT PASSWORD CHANGED",
                              text="Forgot password changed",
                              headers={"REMOTE_ADDR": request.environ["REMOTE_ADDR"],
                                       "HTTP_USER_AGENT": request.environ["HTTP_USER_AGENT"],
                                       "REMOTE_PORT": request.environ["REMOTE_PORT"], }).save())

            user.save()

            logout_session_clear()
            return render_template('auth/password_change_confirmed.html')

    return render_template('auth/password_reset.html',
                           form=form,
                           message=message,
                           require_current=require_current,
                           uid=user.uid,
                           verification_code=verification_code
                           )


@auth_web.route('/change_password', methods=('GET', 'POST'))
@logged_in
def change_password():
    require_current = True
    error = None
    form = PasswordResetForm()

    user = User.objects.filter(uid=session.get('uid')).first()

    if not user:
        abort(404)

    if form.validate_on_submit():
        if user.verify_password(form.current_password.data):
            user.hash_password(form.password.data)
            user.activity.activity_audit.append(
                ActivityAudit(uid=user.uid, created=utc_now(), type='INFO', code="01004 - PASSWORD CHANGE",
                              text="Password changed",
                              headers={"REMOTE_ADDR": request.environ["REMOTE_ADDR"],
                                       "HTTP_USER_AGENT": request.environ["HTTP_USER_AGENT"],
                                       "REMOTE_PORT": request.environ["REMOTE_PORT"], }).save())

            # save the new password
            user.save()
            # log the user out for re-login
            logout_session_clear()
            return render_template('auth/password_change_confirmed.html')
        else:
            error = "Incorrect password"

    return render_template('auth/password_reset.html', form=form, require_current=require_current, error=error)

@auth_web.route('/profile/<updated>', methods=('GET','POST'))
@logged_in
#@cache.cached(timeout=600)
#@nocache
def profile(updated):
    error=None
    user = User.objects.filter(uid=session.get('uid')).first()

    form_avatar  = AvatarForm()
    form_profile = ProfileForm()

    if form_avatar.upload.data and form_avatar.validate_on_submit():
        print("Avatar form submitted")
        if 'file' not in request.files:
            error = 'No file part in the request'

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            error = 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
        
        file.seek(0)
        
        pprint(user.profile)

        user.profile.avatar.replace(file)
        user.profile.updated = utc_now_int()
        user.activity.activity_audit.append(
            ActivityAudit(uid=user.uid, created=utc_now(), type='INFO', code="01006 - AVATAR UPLOADED",
                          text="User avatar added",
                          headers={"REMOTE_ADDR": request.environ["REMOTE_ADDR"],
                                   "HTTP_USER_AGENT": request.environ["HTTP_USER_AGENT"],
                                   "REMOTE_PORT": request.environ["REMOTE_PORT"], }).save())
        user.save()
        session['updated'] = user.profile.updated

    #if form_profile.save.data and form_profile.validate_on_submit():
    if form_profile.save.data:
        print("Profile form submitted")
        user.profile = UserProfile(
                                    updated = utc_now_int(),
                                    first_name = form_profile.first_name.data.strip(),
                                    last_name = form_profile.last_name.data.strip(),
                                    gender = form_profile.gender.data,
                                    date_of_birth = form_profile.date_of_birth.data,
                                    avatar = user.profile.avatar
                                    #interests = form_profile.interests.data.strip().split(),
                                   )        

        user.profile.addresses.append(
            Address(
                created      = utc_now(),
                address_type = 'main',
                door_no_name = form_profile.address_door_no_name.data.strip(),
                street       = form_profile.address_street.data.strip(),
                line_2       = form_profile.address_line2.data.strip(),
                city         = form_profile.address_city.data.strip(),
                county       = form_profile.address_county.data.strip(),
                postcode     = form_profile.address_postcode.data.strip(),
                country      = form_profile.address_country.data.strip(),
            )
        )

        user.activity.activity_audit.append(
            ActivityAudit(uid=user.uid, created=utc_now(), type='INFO', code="01006 - PROFILE UPDATED",
                          text="User profile updated",
                          headers= { "REMOTE_ADDR": request.environ["REMOTE_ADDR"],
                                     "HTTP_USER_AGENT": request.environ["HTTP_USER_AGENT"],
                                     "REMOTE_PORT": request.environ["REMOTE_PORT"],
                                    }
                          ).save())

        user.save()
        
        if form_profile.first_name.data.strip():
            session['first_name'] = form_profile.first_name.data.strip()
        else:
            session.pop('first_name', None)

        return render_template('profile/profile_saved.html')

    # Populate the form when when user loads his profile and then render the template
    if user:
        form_profile.first_name.data = user.profile.first_name
        form_profile.last_name.data = user.profile.last_name
        form_profile.gender.data = user.profile.gender
        form_profile.date_of_birth.data = user.profile.date_of_birth
        if user.profile.addresses:
            user_address = user.profile.addresses[len(user.profile.addresses) - 1]
            form_profile.address_door_no_name.data = user_address.door_no_name
            form_profile.address_street.data = user_address.street
            form_profile.address_line2.data = user_address.line_2
            form_profile.address_city.data = user_address.city
            form_profile.address_county.data = user_address.county
            form_profile.address_postcode.data = user_address.postcode
            form_profile.address_country.data = user_address.country

    return render_template('profile/user_profile.html', form_profile=form_profile, form_avatar=form_avatar)


def avatar_changed():
    if session.get('avatar_changed'):
        print("Avatar has changed")
        return True
    else:
        print("Avatar NOT changed")
        return False

@auth_web.route('/get_avatar_img/<updated>')
@logged_in
#@cache.cached(timeout=600)
#@nocache
def get_avatar_img(updated):
    user = User.objects.filter(uid=session.get('uid')).first()
    if user.profile.avatar:
        img_io =  BytesIO()
        img_io.write(user.profile.avatar.read())
        img_io.seek(0)
        return send_file(img_io, mimetype=user.profile.avatar.content_type)
    else:
        return auth_web.send_static_file('assets/img/no_profile_img.png')

@auth_web.route('/show_avatar')
def show_avatar():
    return render_template('profile/show_avatar.html')


@auth_web.route('/home')
@logged_in
def home():
    user = User.objects.filter(uid=session.get('uid')).first()
    if user:
        if 'admin' in user.authorization.roles:
            # User is administrator
            return render_template('admin/admin_dashboard.html', users=User.objects)
        else:
            # User is normal user
            return render_template('auth/user_loggedon.html')
    else:
        return "WHAT? No user!!! Fishy... Logout" 

    


@auth_web.route('/')
def homepage():
    return render_template('home/index.html')



