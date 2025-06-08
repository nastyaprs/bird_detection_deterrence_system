from flask import render_template, request, redirect, url_for, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models.user import User
from services.user_service import UserService

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db_session = Session()

user_service = UserService(db_session)


def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = user = user_service.authenticate(username, password)
        if user:
            session["user_id"] = user.id
            session["user_name"] = user.name
            return redirect(url_for("index"))
        return render_template("login.html", error="Невірне ім'я користувача або пароль")
    return render_template("login.html")

def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        name = request.form.get("name")
        surname = request.form.get("surname")

        if not all([username, password, email, name, surname]):
            return render_template("register.html", error="Заповніть усі поля")

        existing = user_service.authenticate(username, password)
        if existing:
            return render_template("register.html", error="Користувач з таким іменем вже існує")

        user = user_service.register(username, password, email, name, surname)
        if user:
            session["user_id"] = user.id
            session["user_name"] = user.name
            return redirect(url_for("index"))
        else:
            return render_template("register.html", error="Помилка реєстрації")

    return render_template("register.html")

def logout():
    session.clear()
    return redirect(url_for("login"))
