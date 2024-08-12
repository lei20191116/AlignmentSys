from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, \
    IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email

class AddressForm(FlaskForm):
    address = StringField('地址', validators=[DataRequired()])
    submit = SubmitField('可疑地址搜索')

