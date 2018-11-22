# -*- coding:utf8 -*-

from flask import Flask, render_template, url_for, flash, redirect, request
from forms import Login, StudentRegistration, Settings, InternshipRegistration, SearchStudents, Interview
from flaskext.mysql import MySQL
import logging
import sys
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config["SECRET_KEY"] = "b8cd9b239722889da76ff55e8a2087a5"
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_DB"] = "internship_mng_system"

mysql = MySQL(app)
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

logging.basicConfig(level = logging.ERROR, filename = "error.log", filemode = "a",
                    format = '%(asctime)s:%(levelname)s:%(message)s', datefmt = '%d-%m-%y %H:%M:%S')


@app.route("/")
@app.route("/home")
def home():
    cursor.execute("SELECT * FROM student ORDER BY no ASC LIMIT 10")
    student_list = cursor.fetchall()
    cursor.execute("SELECT COUNT(no) FROM student")
    student_count = cursor.fetchone()
    cursor.execute("SELECT COUNT(no) FROM intern")
    intern_count = cursor.fetchone()
    cursor.execute("SELECT SUM(accepted_day) FROM student")
    total_day = cursor.fetchone()
    cursor.execute("SELECT COUNT(idFirma) FROM firmalar")
    firm_count = cursor.fetchone()

    return render_template("home.html", results = student_list, student_count = student_count,
                           intern_count = intern_count, total_day = total_day, firm_count = firm_count)


## Giriş ekranı
@app.route("/login", methods = ["POST", "GET"])
def login():
    form = Login()
    if form.validate_on_submit():
        if form.username.data == "admin" and form.passwd.data == "1":
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful.", "danger")

    return render_template("login.html", title = "Giriş", form = form)


## Öğrenci listesi
@app.route("/student_list", methods = ["POST", "GET"])
def student_list():
    cursor.execute("SELECT * FROM student")
    results = cursor.fetchall()
    return render_template("student-list.html", title = "Öğrenci Listesi", results = results)


## Öğrenci kayıt sayfası
@app.route("/student_registration", methods = ["POST", "GET"])
def student_registration():
    form = StudentRegistration()
    if form.validate_on_submit():
        try:
            cursor.execute(
                "INSERT INTO student(no, ad, soyad, program, total_day, accepted_day, status, record) VALUES ('" + form.no.data + "','" + form.name.data + "','" + form.surname.data + "','" + form.program.data + "',0, 0, 0, 0)")
            conn.commit()
            flash(u"Öğrenci kaydı başarıyla yapıldı.", "success")
            return redirect(url_for("student_registration"))
        except Exception as e:
            logging.error(e)
            flash(u"Öğrenci daha önce kaydedilmiş.", "danger")
    return render_template("student-registration.html", title = "Öğrenci Kayıt", form = form)


## Staj kayıt sayfası
@app.route("/internship_registration", methods = ["POST", "GET"])
def internship_registration():
    registration_form = InternshipRegistration()
    search_form = SearchStudents()
    results = ""
    no = request.args.get("no")

    cursor.execute("SELECT * FROM sehirler")
    cities = cursor.fetchall()
    registration_form.city.choices = [(city[1], city[1]) for city in cities]
    cursor.execute("SELECT * FROM firmalar ORDER BY firmaAdi ASC")
    firms = cursor.fetchall()
    registration_form.firm.choices = [(firm[1], firm[1]) for firm in firms]
    cursor.execute("SELECT * FROM konular")
    subjects = cursor.fetchall()
    registration_form.subject.choices = [(subject[1], subject[1]) for subject in subjects]

    if no:
        cursor.execute("SELECT * FROM student WHERE no='" + no + "'")
        results = cursor.fetchall()

        if registration_form.validate_on_submit():
            try:
                cursor.execute("INSERT INTO intern(no, konu, kurum, sehir) VALUES ('" + no + "','" + registration_form.subject.data + "','" + registration_form.firm.data + "','" + str(registration_form.city.data) + "')")
                cursor.execute("INSERT INTO randevu(ogrNo) VALUES ('" + no + "')")
                conn.commit()
                return redirect(url_for("internship_registration"))
            except Exception as e:
                logging.error(e)
                flash(u"Bir hata oluştu: " + str(e[1]), "danger")

    return render_template("internship-registration.html", title = "Staj Kaydı", registration_form = registration_form,
                           search_form = search_form, results = results)


## Randevu sayfası
@app.route("/appointment", methods = ["POST", "GET"])
def appointment():
    cursor.execute("SELECT student.no, student.ad, student.soyad, student.program, randevu.tarih, randevu.saat, randevu.ku1, randevu.ku2 FROM intern JOIN randevu ON intern.no=randevu.ogrNo JOIN student ON randevu.ogrNo=student.no WHERE intern.tarih='" + str(datetime.date.today().year) + "' AND intern.degerlendirme=0")
    results = cursor.fetchall()
    return render_template("appointment.html", results = results)


## Mülakat kayıt sayfası
@app.route("/do_interview", methods = ["POST", "GET"])
def do_interview():
    form = Interview()
    return render_template("do-appointment.html", form = form)


## Ayarlar sayfası
@app.route("/settings", methods = ["POST", "GET"])
def settings():
    settings_form = Settings()

    cursor.execute("SELECT * FROM firmalar ORDER BY firmaAdi ASC")
    firms = cursor.fetchall()
    cursor.execute("SELECT * FROM konular")
    subjects = cursor.fetchall()

    subject = request.args.get("new_subject")
    firm = request.args.get("new_firm")

    if subject:
        try:
            cursor.execute(
                "INSERT INTO konular(konu) SELECT * FROM (SELECT '" + subject.upper() + "') AS tmp WHERE NOT EXISTS (SELECT konu FROM konular WHERE konu='" + subject.upper() + "') LIMIT 1 ")
            conn.commit()
            return redirect(url_for("settings"))
        except Exception as e:
            logging.error(e)
    elif firm:
        try:
            cursor.execute(
                "INSERT INTO firmalar(firmaAdi) SELECT * FROM (SELECT '" + firm.upper() + "') AS tmp WHERE NOT EXISTS (SELECT firmaAdi FROM firmalar WHERE firmaAdi='" + firm.upper() + "') LIMIT 1 ")
            conn.commit()
            return redirect(url_for("settings"))
        except Exception as e:
            logging.error(e)

    return render_template("settings.html", title = "Ayarlar", form = settings_form, firms = firms, subjects = subjects)


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0")
