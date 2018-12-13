# -*- coding:utf8 -*-

from flask import Flask, render_template, url_for, flash, redirect, request, session
from forms import Login, StudentRegistration, Settings, InternshipRegistration, SearchStudents, InterviewRegistration, InterviewResult
from flaskext.mysql import MySQL
import logging
import sys
import datetime
import random
import hashlib
import itertools

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

logging.basicConfig(level = logging.ERROR, filename = "error.log", filemode = "a", format = '%(asctime)s:%(levelname)s:%(message)s', datefmt = '%d-%m-%y %H:%M:%S')

@app.route("/")
@app.route("/home")
def home():
    if not session["logged_in"]:
        return redirect(url_for("login"))
    else:
        cursor.execute("SELECT * FROM student ORDER BY no ASC LIMIT 10")
        student_list = cursor.fetchall()
        cursor.execute("SELECT COUNT(no) FROM student")
        student_count = cursor.fetchone()
        cursor.execute("SELECT COUNT(stajID) FROM staj")
        intern_count = cursor.fetchone()
        cursor.execute("SELECT SUM(accepted_day) FROM student")
        total_day = cursor.fetchone()
        cursor.execute("SELECT COUNT(idFirma) FROM firmalar")
        firm_count = cursor.fetchone()
        cursor.execute("SELECT konu FROM konular")
        subject_list = cursor.fetchall()

        return render_template("home.html", results = student_list, student_count = student_count, intern_count = intern_count, total_day = total_day, firm_count = firm_count, subject_list = subject_list)

# Login ekranı
@app.route("/login", methods = ["POST", "GET"])
def login():
    form = Login()

    if form.validate_on_submit():
        try:
            cursor.execute("SELECT parola FROM kullanici WHERE email='%s'" %form.username.data)
            parola = cursor.fetchall()
            if parola[0][0] == str(hashlib.sha256(form.passwd.data).hexdigest()):
                session["logged_in"] = True
                return redirect(url_for("home"))
            else:
                flash("Kullanıcı adı veya parola hatalı.", "danger")
        except Exception as e:
            logging.error(e)
    else:
        logging.error(form.errors)

    return render_template("login.html", title = "Giriş", form = form)

@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("login"))


# Öğrenci listesi
@app.route("/student_list", methods = ["POST", "GET"])
def student_list():
    if not session["logged_in"]:
        return redirect(url_for("login"))
    else:
        cursor.execute("SELECT * FROM student")
        results = cursor.fetchall()

        return render_template("student-list.html", title = "Öğrenci Listesi", results = results)

# Öğrenci detay
@app.route("/student_details", methods = ["POST", "GET"])
def student_details():
    no = request.args.get("no")
    cursor.execute("SELECT * FROM student WHERE no='%s'" %no)
    student_details = cursor.fetchone()
    cursor.execute("SELECT * FROM staj WHERE ogrNo='%s'" %no)
    intern_details = cursor.fetchall()

    return render_template("student-details.html", title="Öğrenci Detay", student_details = student_details, intern_details = intern_details)

# Öğrenci kayıt sayfası
@app.route("/student_registration", methods = ["POST", "GET"])
def student_registration():
    if not session["logged_in"]:
        return redirect(url_for("login"))
    else:
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


# Staj listesi
@app.route("/intern_list", methods = ["POST", "GET"])
def intern_list():
    if not session["logged_in"]:
        return redirect(url_for("login"))
    else:
        cursor.execute(
            "SELECT s.no, s.ad, s.soyad, staj.sinif, staj.firma, staj.sehir, staj.konu, staj.basTarih, staj.bitTarih, staj.gun, staj.stajID FROM student s JOIN staj ON s.no=staj.ogrNo ")
        results = cursor.fetchall()

        return render_template("intern-list.html", title = "Staj Listesi", results = results)


# Staj kayıt sayfası
@app.route("/internship_registration", methods = ["POST", "GET"])
def internship_registration():
    if not session["logged_in"]:
        return redirect(url_for("login"))
    else:
        registration_form = InternshipRegistration()
        search_form = SearchStudents()
        results = ""
        no = request.args.get("no")
        # firm = request.args.get("new_firm")

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

                    if registration_form.day.data < 15:
                        flash(u"15 günden az staj yapılamaz.", "danger")
                    elif registration_form.grade.data == 2 and registration_form.day.data > 25:
                        flash(u"2. sınıf öğrencileri 25 günden fazla staj yapamaz.", "danger")
                    elif registration_form.subject.data != "AR-GE" and registration_form.day.data > 40:
                        flash(u"Konusu AR-GE olmayan stajların gün sayısı 40'tan fazla olamaz.", "danger")
                    elif registration_form.subject.data == "AR-GE" and registration_form.day.data > 60:
                        flash(u"AR-GE konulu stajlar en fazla 60 gün olabilir.", "danger")
                    else:
                        try:
                            cursor.execute(
                                "INSERT INTO staj(stajID, ogrNo, firma, sehir, konu, gun, basTarih, bitTarih, sinif, degerlendirme) VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (stajID, no, registration_form.firm.data, str(registration_form.city.data),
                                registration_form.subject.data, str(registration_form.day.data), start_date, end_date,
                                str(registration_form.grade.data), "0"))
                            conn.commit()
                            cursor.execute("SELECT total_day FROM student WHERE no='%s'" %no)
                            result = cursor.fetchone()
                            total_day = result[0] + registration_form.day.data
                            cursor.execute("UPDATE student SET total_day='%d' WHERE no='%s'" %(total_day, no))
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

        return render_template("internship-registration.html", title = "Staj Kaydı", registration_form = registration_form, search_form = search_form, results = results)


# Mülakat kayıt sayfası
@app.route("/interview_registration", methods = ["POST", "GET"])
def interview_registration():
    if not session["logged_in"]:
        return redirect(url_for("login"))
    else:
        form = InterviewRegistration()
        staj_id = request.args.get("staj_id")

        cursor.execute("SELECT * FROM komisyon_uyeleri ORDER BY ad DESC")
        members = cursor.fetchall()
        form.ku1.choices = [(member[1], member[1]) for member in members]
        form.ku2.choices = [(member[1], member[1]) for member in members]

        if form.validate_on_submit():
            date = str(form.date.data)[-2:] + "-" + str(form.date.data)[5:7] + "-" + str(form.date.data)[:4]
            try:
                cursor.execute("INSERT INTO mulakat(stajID, tarih, saat, ku1, ku2) VALUES ('%s', '%s', '%s', '%s', '%s')" % (staj_id, date, form.time.data, form.ku1.data, form.ku2.data))
                conn.commit()
                return redirect(url_for("intern_list"))
            except Exception as e:
                logging.error(e)
                flash(u"Bir hata oluştu", "danger")

        return render_template("interview-registration.html", title = "Mülakat Kaydı", form = form)


# Mülakat listesi
@app.route("/interview_list", methods = ["POST", "GET"])
def interview_list():
    if not session["logged_in"]:
        return redirect(url_for("login"))
    else:
        cursor.execute("SELECT st.no, st.ad, st.soyad, st.program, m.tarih, m.saat, m.ku1, m.ku2, m.mulakatID FROM mulakat m JOIN staj s ON m.stajID=s.stajID JOIN student st ON s.ogrNo=st.no")
        results = cursor.fetchall()

        return render_template("interview-list.html", results=results)


# Mülakat kayıt sayfası
@app.route("/do_interview", methods = ["POST", "GET"])
def do_interview():
    if not session["logged_in"]:
        return redirect(url_for("login"))
    else:
        form = InterviewResult()
        mulakat_id = request.args.get("mulakat")
        gun_sayisi = 0

        if form.validate_on_submit():
            devam = form.devam.data * 20 * 0.04
            caba = form.caba.data * 20 * 0.04
            vakit = form.vakit.data * 20 * 0.04
            amir_davranis = form.amir_davranis.data * 20 * 0.04
            ark_davranis = form.ark_davranis.data * 20 * 0.04
            prove = form.prove.data * 0.15
            duzen = form.duzen.data * 0.05
            sunum = form.sunum.data * 0.05
            icerik = form.icerik.data * 0.15
            mulakat = form.mulakat.data * 0.4

            puan = devam + caba + vakit + amir_davranis + ark_davranis + prove + duzen + sunum + icerik + mulakat

            try:
                cursor.execute("SELECT gun, ogrNo FROM staj WHERE stajID=(SELECT stajID FROM mulakat WHERE mulakatID='%s')" %mulakat_id)
                results = cursor.fetchall()
                kabul_gun = int(int(results[0][0]) * puan / 100)
                cursor.execute("SELECT accepted_day FROM student WHERE no='%s'" % results[0][1])
                eski_kabul_gun = cursor.fetchone()
                cursor.execute("UPDATE student SET accepted_day='%d' WHERE no='%s'" % (eski_kabul_gun[0] + kabul_gun, results[0][1]))
                conn.commit()

                if (eski_kabul_gun[0] + kabul_gun) >= 57:
                    cursor.execute("UPDATE student SET status=1 WHERE no='%s'" %results[0][1])
                    conn.commit()
                return redirect(url_for("interview_list"))
            except Exception as e:
                logging.error(e)
        else:
            logging.error(form.errors)

        return render_template("do-interview.html", form = form)

@app.route("/interview_result", methods = ["POST", "GET"])
def interview_result():
    year = request.args.get("year")

    cursor.execute("SELECT DISTINCT RIGHT(tarih, 4) FROM mulakat")
    years = cursor.fetchall()

    cursor.execute("SELECT student.no, student.ad, student.soyad, staj.firma, staj.gun, mulakat.sonuc FROM mulakat JOIN staj ON staj.stajID=mulakat.stajID JOIN student ON staj.ogrNo=student.no WHERE RIGHT(mulakat.tarih, 4) = '%s'" %year)
    results = cursor.fetchall()

    return render_template("interview-result.html", years = years, results = results)


# Ayarlar sayfası
@app.route("/settings", methods = ["POST", "GET"])
def settings():
    if not session["logged_in"]:
        return redirect(url_for("login"))
    else:
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

        return render_template("settings.html", title = "Ayarlar", form = settings_form, firms = firms, subjects = subjects, members = members)

@app.route("/statistics", methods = ["POST", "GET"])
def statistics():
    # cursor.execute("SELECT DISTINCT RIGHT(basTarih, 4) FROM staj ORDER BY RIGHT(basTarih, 4) ASC")
    # labels = cursor.fetchall()
    #
    # cursor.execute("SELECT konu FROM konular")
    # subjects = cursor.fetchall()
    #
    # cursor.execute("SELECT RIGHT(basTarih,4), konu, COUNT(stajID) FROM staj GROUP BY RIGHT(basTarih,4), konu ORDER BY RIGHT(basTarih,4) ASC")
    # results = cursor.fetchall()
    #
    # values = []
    # s = []
    # l = []
    #
    # for i in subjects:
    #     s.append(i[0])
    #
    # for i in labels:
    #     l.append(i[0])
    #
    # old_year = 0
    # for result in results:
    #     if old_year != result[0]:
    #         values.extend(4*[0])
    #         old_year = result[0]
    #
    #     index = l.index(result[0]) * 4 + s.index(result[1])
    #     values[index] = result[2]

    cursor.execute("SELECT konu, COUNT(konu) FROM staj GROUP BY konu")
    results = cursor.fetchall()

    return render_template("statistics.html", title="İstatistikler", results = results)

if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0")
