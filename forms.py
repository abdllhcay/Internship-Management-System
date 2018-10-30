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
    no = StringField(u"Öğrenci No", validators = [DataRequired()])
    name = StringField(u"Ad", validators = [DataRequired()])
    surname = StringField(u"Soyad", validators = [DataRequired()])
    program = SelectField(u"Program", choices = [("1", u"1. Öğretim"), ("2", u"2. Öğretim")])


class SettingsForm(FlaskForm):
    branch = StringField("Konu")
    members = StringField("Komisyon Üyesi")
    date = DateField("Tarih", format = '%d-%m-%Y')
    firm = StringField("Kurum")


class InternshipRegistrationForm(FlaskForm):
    no = StringField(u"Öğrenci No", validators = [DataRequired()])
    name = StringField(u"Ad", validators = [DataRequired()])
    surname = StringField(u"Soyad", validators = [DataRequired()])
    program = SelectField(u"Program", choices = [("1", u"1. Öğretim"), ("2", u"2. Öğretim")])
    grade = IntegerField(u"Sınıf", validators = [DataRequired()])
    firm = SelectField(u"Kurum Adı", choices = [("bga", "BGA"), ("linspark", "LINSPARK")])
    city = SelectField(u"Şehir", choices = [("ist", "ISTANBUL")])
    date = DateField(u"Tarih Aralığı", format = "%d-%m-%Y", validators = [DataRequired()])
    day = IntegerField(u"Gün Sayısı", validators = [DataRequired()])
    subject = SelectField(u"Konu", choices = [("yazilim", "YAZILIM")])

class SearchStudents(FlaskForm):
    search = StringField('search', [DataRequired()])
    submit = SubmitField('Search', render_kw = {'class': 'btn btn-success btn-block'})
