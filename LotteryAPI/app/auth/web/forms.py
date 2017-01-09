from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.widgets.core import HTMLString, html_params
from wtforms.widgets import TextArea
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import ValidationError
from flask_wtf.file import FileField, FileAllowed
import reference_data
import re

from app.auth.models import User

class BaseUserForm(Form):
    email = EmailField('Email address', [
        validators.DataRequired(),
        validators.Email()
        ]
    )

class PasswordBaseForm(Form):
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.length(min=4, max=80)
        ])
    confirm = PasswordField('Repeat Password')


class RegisterForm(BaseUserForm, PasswordBaseForm):
    def validate_email(form, field):
        if User.objects.filter(email=field.data).first():
            raise ValidationError("Email is already in use")

#class RegisterForm(Form):
#    email = EmailField('Email address', [
#        validators.DataRequired(),
#        validators.Email()
#    ]
#                       )
#    password = PasswordField('New Password', [
#        validators.Required(),
#        validators.EqualTo('confirm', message='Passwords must match'),
#        validators.length(min=4, max=80)
#    ])
#    confirm = PasswordField('Repeat Password')
#
#    def validate_email(form, field):
#        if app.auth.models.User.objects.filter(email=field.data).first():
#            raise ValidationError("Email is already in use")

class LoginForm(Form):
    email = EmailField('Email address', [
        validators.DataRequired(),
        validators.length(min=4, max=25)
        ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.length(min=4, max=80)
        ])
    remember_me = BooleanField('Remember me')


class EditForm(BaseUserForm):
    image = FileField('Profile image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'],
                    'Only JPEG, PNG and GIFs allowed')
    ])


class ForgotForm(Form):
    email = EmailField('Email address',
                       [validators.DataRequired(), validators.Email()]
                       )


class PasswordResetForm(PasswordBaseForm):
    current_password = PasswordField('Current Password',
                                     [validators.DataRequired(),
                                      validators.Length(min=4, max=80)]
                                     )

# Custom form for profile fields where it will be readonly and
#   upon clicking edit it will turn into changeable field



class clickEditField(StringField):
    #def __init__(self, error_class=u'has_errors'):
    #    super(clickEditField, self).__init__()
    #    self.error_class = error_class

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop('class', '') or kwargs.pop('class_', '')
            kwargs['class'] = u'%s %s' % (self.error_class, c)
        return super(clickEditField, self).__call__(field, **kwargs)



class ProfileForm(Form):
    first_name = StringField('First Name', [
        validators.DataRequired(),
        validators.length(min=1, max=50)
    ])
    last_name = StringField('Last Name', [
        validators.DataRequired(),
        validators.length(min=1, max=50)
    ])
    gender = SelectField('Gender', choices=[('','Please select gender'), ('M', 'Male '), ('F', 'Female')])
    date_of_birth = DateField('Date of Birth')
    #interests = StringField('Interests')

    address_door_no_name = StringField('Door/House', [validators.DataRequired()])
    address_street = StringField('Street', [validators.DataRequired()])
    address_line2 = StringField('2nd Line')
    address_city = StringField('City', [validators.DataRequired()])
    address_county = SelectField('County', choices=reference_data.uk_counties)
    address_postcode = StringField('Postcode', [validators.DataRequired()])
    address_country = SelectField('Country', choices=reference_data.countries, default="GB")

    save = SubmitField('Save')
    cancel = SubmitField('Cancel')


class AvatarForm(Form):
    file = FileField('Change photo',[validators.DataRequired()])
    upload = SubmitField('Upload')
