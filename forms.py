# -*- coding:utf8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired


class Login(FlaskForm):
    username = StringField("Kullanici Adi", validators = [DataRequired()])
    passwd = PasswordField("Parola", validators = [DataRequired()])
    remember = BooleanField("Beni hatirla")
    submit = SubmitField("Giris")


class StudentRegistration(FlaskForm):
    no = StringField(u"Öğrenci No", validators = [DataRequired()])
    name = StringField(u"Ad", validators = [DataRequired()])
    surname = StringField(u"Soyad", validators = [DataRequired()])
    program = SelectField(u"Program", choices = [("1", u"1. Öğretim"), ("2", u"2. Öğretim")])


class Settings(FlaskForm):
    members = StringField(u"Komisyon Üyesi")
    date = DateField("Tarih", format = '%d-%m-%Y')
    firm = SelectField("Kurum")
    subject = SelectField("Konu")
    add_firm = StringField("Kurum")
    add_subject = StringField("Konu")


class InternshipRegistration(FlaskForm):
    grade = IntegerField(u"Sınıf", validators = [DataRequired()])
    firm = SelectField(u"Kurum Adı", choices = [("bga", "BGA"), ("linspark", "LINSPARK")])
    city = SelectField(u"Şehir")
    date = StringField(u"Tarih Aralığı", validators = [DataRequired()])
    day = IntegerField(u"Gün Sayısı", validators = [DataRequired()])
    subject = SelectField(u"Konu", choices = [("yazilim", "YAZILIM")])


class SearchStudents(FlaskForm):
    no = StringField('no', validators = [DataRequired()])
    submit = SubmitField('Search', render_kw = {'class': 'btn btn-success btn-block'})


class Interview(FlaskForm):
    continuity = SelectField(u"Devam", choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default = 5,
                             validators = [DataRequired()])
    work = SelectField(u"Çaba ve çalışma", choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default = 5,
                       validators = [DataRequired()])
    time = SelectField(u"İşi vaktinde yapma", choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default = 5,
                       validators = [DataRequired()])
    chief = SelectField(u"Amire karşı davranış", choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default = 5,
                        validators = [DataRequired()])
    co_worker = SelectField(u"İş arkadaşlarına karşı davranış", choices = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                            default = 5, validators = [DataRequired()])
    prove = IntegerField(u"İspat", validators = [DataRequired()])
    order = IntegerField(u"Düzen", validators = [DataRequired()])
    presentation = IntegerField(u"Sunum", validators = [DataRequired()])
    content = IntegerField(u"İçerik", validators = [DataRequired()])
    interview = IntegerField(u"Mülakat", validators = [DataRequired()])
