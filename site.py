# -*- coding:utf8 -*-

from flask import Flask, render_template, url_for, flash, redirect, request
from forms import Login, StudentRegistration, Settings, InternshipRegistration, SearchStudents, Interview, Appointment
from flaskext.mysql import MySQL
import logging
import sys
import datetime
import random

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
                "INSERT INTO student(no, ad, soyad, program, total_day, accepted_day, status, record) VALUES ('%s', '%s', '%s', '%s', 0, 0, 0, 0)" % (
                form.no.data, form.name.data, form.surname.data, form.program.data))
            conn.commit()
            flash(u"Öğrenci kaydı başarıyla yapıldı.", "success")
            return redirect(url_for("student_registration"))
        except Exception as e:
            logging.error(e)
            flash(u"Bir hata oluştu! Öğrenci daha önce kaydedildi mi?", "danger")
    return render_template("student-registration.html", title = "Öğrenci Kayıt", form = form)


## Staj kayıt sayfası
@app.route("/internship_registration", methods = ["POST", "GET"])
def internship_registration():
    registration_form = InternshipRegistration()
    search_form = SearchStudents()
    results = ""
    no = request.args.get("no")
    #firm = request.args.get("new_firm")

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

        if results:
            if registration_form.validate_on_submit():
                stajID = random.randint(100000000, 999999999)
                start_date = str(registration_form.start_date.data)[-2:] + "-" + str(registration_form.start_date.data)[5:7] + "-" + str(registration_form.start_date.data)[:4]
                end_date = str(registration_form.finish_date.data)[-2:] + "-" + str(registration_form.finish_date.data)[5:7] + "-" + str(registration_form.finish_date.data)[:4]
                try:
                    cursor.execute("INSERT INTO staj(stajID, ogrNo, firma, sehir, konu, gun, basTarih, bitTarih, sinif, degerlendirme) VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(stajID, no, registration_form.firm.data, str(registration_form.city.data), registration_form.subject.data, str(registration_form.day.data), start_date, end_date, str(registration_form.grade.data), "0"))
                    cursor.execute("INSERT INTO randevu(ogrNo) VALUES ('%s')" %no)
                    conn.commit()
                    flash(u"Staj kaydı başarıyla yapıldı.", "success")
                    return redirect(url_for("internship_registration"))
                except Exception as e:
                    logging.error(e)
                    flash(u"Bir hata oluştu", "danger")
        else:
            flash(u"Öğrenci bulunamadı!", "danger")

    # elif firm:
    #     try:
    #         cursor.execute(
    #             "INSERT INTO firmalar(firmaAdi) SELECT * FROM (SELECT '" + firm.upper() + "') AS tmp WHERE NOT EXISTS (SELECT firmaAdi FROM firmalar WHERE firmaAdi='" + firm.upper() + "') LIMIT 1 ")
    #         conn.commit()
    #         return redirect(url_for("settings"))
    #     except Exception as e:
    #         logging.error(e)

    return render_template("internship-registration.html", title = "Staj Kaydı", registration_form = registration_form,
                           search_form = search_form, results = results)


## Randevu sayfası
@app.route("/appointment", methods = ["POST", "GET"])
def appointment():
    appointment_form = Appointment()

    cursor.execute("SELECT * FROM komisyon_uyeleri ORDER BY ad DESC")
    members = cursor.fetchall()
    appointment_form.ku1.choices=[(member[1], member[1]) for member in members]
    appointment_form.ku2.choices = [(member[1], member[1]) for member in members]

    if appointment_form.validate_on_submit():
        try:
            cursor.execute("UPDATE randevu SET tarih='%s', saat='%s', ku1='%s', ku2='%s' WHERE ogrNo='%s'" % (appointment_form.date.data, appointment_form.time.data, appointment_form.ku1.data, appointment_form.ku2.data, appointment_form.ogr_no.data))
            conn.commit()
        except Exception as e:
            logging.error(e)
    try:
        cursor.execute(
            "SELECT student.no, student.ad, student.soyad, student.program, randevu.tarih, randevu.saat, randevu.ku1, randevu.ku2 FROM staj JOIN randevu ON staj.ogrNo=randevu.ogrNo JOIN student ON randevu.ogrNo=student.no WHERE staj.basTarih='%s' AND staj.degerlendirme=0" % datetime.date.today().year)
        results = cursor.fetchall()
    except Exception as e:
        logging.error(e)

    return render_template("appointment.html", results = results, appointment_form = appointment_form)


## Mülakat kayıt sayfası
@app.route("/do_interview", methods = ["POST", "GET"])
def do_interview():
    form = Interview()
    return render_template("do-interview.html", form = form)


## Ayarlar sayfası
@app.route("/settings", methods = ["POST", "GET"])
def settings():
    settings_form = Settings()

    cursor.execute("SELECT * FROM firmalar ORDER BY firmaAdi ASC")
    firms = cursor.fetchall()
    cursor.execute("SELECT * FROM konular")
    subjects = cursor.fetchall()
    cursor.execute("SELECT * FROM komisyon_uyeleri ORDER BY ad DESC")
    members = cursor.fetchall()

    subject = request.args.get("new_subject")
    firm = request.args.get("new_firm")
    member = request.args.get("new_member")

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
    elif member:
        try:
            cursor.execute(
                "INSERT INTO komisyon_uyeleri(ad) SELECT * FROM (SELECT '" + member.upper() + "') AS tmp WHERE NOT EXISTS (SELECT ad FROM komisyon_uyeleri WHERE ad='" + member.upper() + "') LIMIT 1 ")
            conn.commit()
            return redirect(url_for("settings"))
        except Exception as e:
            logging.error(e)

    return render_template("settings.html", title = "Ayarlar", form = settings_form, firms = firms, subjects = subjects,
                           members = members)


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0")
