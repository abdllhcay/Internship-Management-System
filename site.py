# -*- coding:utf8 -*-

from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, StudentRegistrationForm, SettingsForm, InternshipRegistrationForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "b8cd9b239722889da76ff55e8a2087a5"


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


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
    return render_template("student-list.html", title = "Öğrenci Listesi")


@app.route("/student_registration", methods = ["POST", "GET"])
def student_registration():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        pass

    return render_template("student-registration.html", title = "Öğrenci Kayıt", form = form)


@app.route("/internship_registration", methods = ["POST", "GET"])
def internship_registration():
    form = InternshipRegistrationForm()
    return render_template("internship-registration.html", title = "Staj Kaydı", form = form)


@app.route("/settings", methods = ["POST", "GET"])
def settings():
    form = SettingsForm()

    return render_template("settings.html", title = "Ayarlar", form = form)


if __name__ == "__main__":
    app.run(debug = True)
