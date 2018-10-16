# -*- coding:utf8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    username = StringField("Kullanici Adi", validators = [DataRequired()])
    passwd = PasswordField("Parola", validators = [DataRequired()])
    remember = BooleanField("Beni hatirla")
    submit = SubmitField("Giris")


class StudentRegistrationForm(FlaskForm):
    no = IntegerField("Ogrenci No", validators = [DataRequired()])
    name = StringField("Ad", validators = [DataRequired()])
    surname = StringField("Soyad", validators = [DataRequired()])
    program = SelectField("Program", choices = [("1", "1. Ogretim"), ("2", "2. Ogretim")])


class SettingsForm(FlaskForm):
    branch = StringField("Konu")
    members = StringField("Komisyon Üyesi")
    date = DateField("Tarih", format = '%d-%m-%Y')
    firm = StringField("Kurum")


class InternshipRegistrationForm(FlaskForm):
    grade = IntegerField(u"Sınıf", validators = [DataRequired()])
    firm = SelectField(u"Kurum Adı", choices = [("bga", "BGA"), ("linspark", "LINSPARK")])
    city = SelectField(u"Şehir", choices = [("ist", "ISTANBUL")])
    date = DateField(u"Tarih Aralığı", format = "%d-%m-%Y", validators = [DataRequired()])
    day = IntegerField(u"Gün Sayısı", validators = [DataRequired()])
    subject = SelectField(u"Konu", choices = [("yazilim", "YAZILIM")])
