from datetime import date
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required

from petitcalendrier import app, bcrypt, db 
from petitcalendrier.forms import LoginForm, RegisterForm, AnswerForm
from petitcalendrier.models import User, Answer, Question

@app.route("/")
@login_required
def home():
    today = date.today()
    days = [14, 10, 11, 8, 22, 18, 21, 23, 16, 13, 5, 17, 3, 1, 9, 6, 7, 24, 12, 19, 15, 20, 2, 4]
    open_gifts = {day for day in range(1, today.day)}
    todays_question = Question.query.filter_by(day=today.day).first()
    score = current_user.score
    if todays_question:
        answer = Answer.query.filter_by(question=todays_question, author=current_user).first()
        if answer:
            open_gifts.add(today.day)
    return render_template("home.j2", first_name=current_user.first_name, days=days, open_gifts=open_gifts, score=score, today=today)

@app.route("/day/<int:day>", methods=['GET', 'POST'])
@login_required
def day(day):
    score=current_user.score
    if day < 1 or day > 24: 
        abort(404)
    question = Question.query.filter_by(day=day).first_or_404()
    challenge = url_for('static', filename=f'images/cases/{question.image}')
    answer = Answer.query.filter_by(question=question, author=current_user).first()
    today = date.today()
    if day == today.day: 
        form = AnswerForm()
        if form.validate_on_submit():
            answer = create_answer(form, question, current_user)
            db.session.add(answer)
            db.session.commit()
            flash(f"Merci d'avoir répondu à la question du jour", "success")
            if (answer.answer_character == question.answer): 
                score+=20; 
            else:
                score +=1
            current_user.score = score
            db.session.commit()
            return render_template("gift.j2", day=day, challenge=challenge, answer=answer, question=question, expired=True, score=score, today=today)
        return render_template("gift.j2", day=day, form=form, challenge=challenge, answer=answer, question=question, expired=False, score=score)
    elif day < today.day: 
        return render_template("gift.j2", day=day, challenge=challenge, answer=answer, question=question, expired=True, score=score)
    elif day > today.day: 
        return redirect(url_for('home'))
        

def create_answer(form, question, user):
    character = form.answer_character.data
    time = form.answer_time.data
    object = form.answer_object.data 
    place = form.answer_place.data
    sound = form.answer_sound.data
    color = form.answer_color.data
    return Answer(answer_character=character, answer_time=time, answer_object=object, answer_place=place, answer_sound=sound, answer_color=color, question=question, author=user)

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
            flash("Mauvais nom d'utilisateur ou mot de passe", "danger")

    return render_template("login.j2", form=form)

@app.route("/users/new", methods=['GET', 'POST'])
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
        return redirect(url_for("register"))

    return render_template("register.j2", form=form, title="Créer un utilisateur")

@app.route("/users/update/<int:user_id>", methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.filter_by(id=user_id).first_or_404()
    form = RegisterForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        db.session.commit()
        flash('Utilisateur modifié', 'success')
        return url_for('users')
    elif request.method == 'GET':
        form.username.data = user.username
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
    return render_template("register.j2", title=f"Modifier l'utilisateur {user.username}", form=form)


@app.route("/users")
@login_required
def users():
    if not current_user.is_admin:
        abort(403)
    users = User.query.all()
    return render_template("users.j2", users=users)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/score")
@login_required
def score():
    users = User.query.order_by(User.score.desc()).all()  
    return render_template("score.j2", users=users)


@app.route("/apropos")
def apropos():
    return render_template("apropos.j2")