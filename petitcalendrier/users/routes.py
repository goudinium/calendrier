from flask import Blueprint, render_template, redirect, url_for, abort, request, flash
from flask_login import current_user, login_required, login_user, logout_user

from petitcalendrier.users.forms import RegisterForm, LoginForm
from petitcalendrier.models import User, Answer
from petitcalendrier import bcrypt, db 

users = Blueprint('users', __name__)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('calendar.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('calendar.home'))
        else:
            flash("Mauvais nom d'utilisateur ou mot de passe", "danger")

    return render_template("login.j2", form=form)

@users.route("/users/new", methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.is_admin:
        abort(403)
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Utilisateur créé avec succès", "success")
        return redirect(url_for("users.register"))

    return render_template("register.j2", form=form, title="Créer un utilisateur")

@users.route("/users/<int:user_id>")
@login_required
def check_answers(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.filter_by(id=user_id).first_or_404()
    answers = user.answers
    return render_template("answers_by_user.j2", user=user, answers=answers)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route("/users")
@login_required
def users_list():
    if not current_user.is_admin:
        abort(403)
    users = User.query.all()
    return render_template("users.j2", users=users)
