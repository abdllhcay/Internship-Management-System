# -*- coding:utf8 -*-

from flask import Flask, render_template, url_for, flash, redirect, request
from forms import LoginForm, StudentRegistrationForm, SettingsForm, InternshipRegistrationForm, SearchStudents
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config["SECRET_KEY"] = "b8cd9b239722889da76ff55e8a2087a5"
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_DB"] = "internship_mng_system"

mysql = MySQL(app)
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()


@app.route("/")
@app.route("/home")
def home():
    cursor.execute("SELECT * FROM student ORDER BY no ASC LIMIT 10")
    results = cursor.fetchall()

    return render_template("home.html", results = results)


@app.route("/login", methods = ["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "admin" and form.passwd.data == "1":
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful.", "danger")

    return render_template("login.html", title = "Giriş", form = form)


@app.route("/student_list", methods = ["POST", "GET"])
def student_list():
    cursor.execute("SELECT * FROM student")
    results = cursor.fetchall()
    return render_template("student-list.html", title = "Öğrenci Listesi", results = results)


@app.route("/student_registration", methods = ["POST", "GET"])
def student_registration():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        try:
            cursor.execute(
                "INSERT INTO student(no, ad, soyad, program, total_day, accepted_day, status, record) VALUES ('" + form.no.data + "','" + form.name.data + "','" + form.surname.data + "','" + form.program.data + "',0, 0, 0, 0)")
            conn.commit()
            flash(u"Öğrenci kaydı başarıyla yapıldı.", "success")
            return redirect(url_for("student_registration"))
        except:
            flash(u"Öğrenci daha önce kaydedilmiş.", "danger")
    return render_template("student-registration.html", title = "Öğrenci Kayıt", form = form)


@app.route("/internship_registration", methods = ["POST", "GET"])
def internship_registration():
    registration_form = InternshipRegistrationForm()
    search_form = SearchStudents()
    results = ""

    if registration_form.validate_on_submit():
        pass
    elif search_form.validate_on_submit():
        cursor.execute("SELECT * FROM student WHERE no='" + search_form.search.data + "'")
        results = cursor.fetchall()

    return render_template("internship-registration.html", title = "Staj Kaydı", registration_form = registration_form,
                           search_form = search_form, results = results)


@app.route("/settings", methods = ["POST", "GET"])
def settings():
    form = SettingsForm()
    return render_template("settings.html", title = "Ayarlar", form = form)


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0")
