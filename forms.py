# -*- coding:utf8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    username = StringField("Kullanici Adi", validators = [DataRequired()])
    passwd = PasswordField("Parola", validators = [DataRequired()])
    remember = BooleanField("Beni hatirla")
    submit = SubmitField("Giris")


class StudentRegistrationForm(FlaskForm):
    number = IntegerField("Öğrenci No", validators = [DataRequired()])
    name = StringField("Ad", validators = [DataRequired()])
    surname = StringField("Soyad", validators = [DataRequired()])
    program = SelectField("Program", choices = [("1", "1. Öğretim"), ("2", "2. Öğretim")])
