# -*- coding:utf8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, DateField, HiddenField
from wtforms.validators import DataRequired


class Login(FlaskForm):
    username = StringField(u"Kullanıcı Adı", validators = [DataRequired()])
    passwd = PasswordField("Parola", validators = [DataRequired()])
    remember = BooleanField(u"Beni hatırla")
    submit = SubmitField("Giris")

class StudentRegistration(FlaskForm):
    no = StringField(u"Öğrenci No", validators = [DataRequired()])
    name = StringField(u"Ad", validators = [DataRequired()])
    surname = StringField(u"Soyad", validators = [DataRequired()])
    program = SelectField(u"Program", choices = [("1", u"1. Öğretim"), ("2", u"2. Öğretim")])
    dgs = BooleanField(u"DGS")

class Settings(FlaskForm):
    new_member = StringField(u"Komisyon Üyesi")
    new_firm = StringField("Kurum")
    new_subject = StringField("Konu")

class InternshipRegistration(FlaskForm):
    grade = IntegerField(u"Sınıf", validators = [DataRequired()])
    firm = SelectField(u"Firma Adı")
    new_firm = StringField(u"Firma ekle")
    city = SelectField(u"Şehir")
    start_date = DateField(u"Başlangıç Tarihi", validators = [DataRequired()])
    finish_date = DateField(u"Bitiş Tarihi", validators = [DataRequired()])
    day = IntegerField(u"Gün Sayısı", validators = [DataRequired()])
    subject = SelectField(u"Konu")

class SearchStudents(FlaskForm):
    no = StringField('no', validators = [DataRequired()])
    submit = SubmitField('Search', render_kw = {'class': 'btn btn-success btn-block'})

class InterviewResult(FlaskForm):
    devam = SelectField(u"Devam", choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default = 5, coerce=int)
    caba = SelectField(u"Çaba ve çalışma", choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default = 5, coerce=int)
    vakit = SelectField(u"İşi vaktinde yapma", choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default = 5, coerce=int)
    amir_davranis = SelectField(u"Amire karşı davranış", choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default = 5, coerce=int)
    ark_davranis = SelectField(u"İş arkadaşlarına karşı davranış", choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default = 5, coerce=int)
    prove = IntegerField(u"İspat", validators = [DataRequired()])
    duzen = IntegerField(u"Düzen", validators = [DataRequired()])
    sunum = IntegerField(u"Sunum", validators = [DataRequired()])
    icerik = IntegerField(u"İçerik", validators = [DataRequired()])
    mulakat = IntegerField(u"Mülakat", validators = [DataRequired()])

class InterviewRegistration(FlaskForm):
    date = DateField(u"Tarih", validators = [DataRequired()])
    time = StringField(u"Saat", validators = [DataRequired()])
    ku1 = SelectField(u"Komisyon üyesi 1", validators = [DataRequired()])
    ku2 = SelectField(u"Komisyon üyesi 2", validators = [DataRequired()])