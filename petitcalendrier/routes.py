from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required


from petitcalendrier import app, bcrypt, db 
from petitcalendrier.forms import LoginForm, RegisterForm
from petitcalendrier.models import User

@app.route("/")
@login_required
def home():
    return render_template("home.j2")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Mauvais nom d'utilisateur ou mot de passe")

    return render_template("login.j2", form=form)

@app.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Utilisateur créé avec succès", "success")
        return redirect(url_for("register"))

    return render_template("register.j2", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))