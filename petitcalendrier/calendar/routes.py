from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import current_user, login_required

from petitcalendrier import get_todays_day, db
from petitcalendrier.models import Question, Answer, User
from petitcalendrier.calendar.forms import AnswerForm
from petitcalendrier.calendar.utils import create_answer

calendar = Blueprint('calendar', __name__)

@calendar.route("/")
@calendar.route("/calendar")
@login_required
def home():
    today = get_todays_day()
    days = [12, 8, 7, 5, 11, 24, 20, 1, 23, 13, 6, 19, 15, 4, 2, 18, 10, 22, 9, 21, 3, 16, 17, 14]
    open_gifts = {day for day in range(1, today)}
    todays_question = Question.query.filter_by(day=today).first()
    score = current_user.score
    if todays_question:
        answer = Answer.query.filter_by(question=todays_question, author=current_user).first()
        if answer:
            open_gifts.add(today)
    return render_template("home.j2", first_name=current_user.first_name, days=days, open_gifts=open_gifts, score=score, today=today)

@calendar.route("/day/<int:day>", methods=['GET', 'POST'])
@login_required
def day(day):
    score=current_user.score
    if day < 1 or day > 24: 
        abort(404)
    question = Question.query.filter_by(day=day).first_or_404()
    challenge = url_for('static', filename=f'images/cases/{question.image}.png')
    answer = Answer.query.filter_by(question=question, author=current_user).first()
    today = get_todays_day()
    if day == today and answer == None: 
        form = AnswerForm()
        if form.validate_on_submit():
            answer = create_answer(form, question, current_user)
            db.session.add(answer)
            db.session.commit()
            if (answer.answer_character == question.answer): 
                score+=7 
            else:
                score +=2
            current_user.score = score
            db.session.commit()
            return redirect(url_for("calendar.day", day=day))
        return render_template("todays_gift_without_answer.j2", form=form, challenge=challenge, day=day)
    elif day == today and answer != None:
        return render_template("todays_gift_with_answer.j2", day=day, challenge=challenge, answer=answer, day_before=day-1)
    elif day < today and answer: 
        return render_template("old_gift_with_answer.j2", day=day, answer=answer, question=question, challenge=challenge)
    elif day < today and not answer:
        return render_template("old_gift_without_answer.j2", day=day, challenge=challenge, question=question)
    elif day > today: 
        return redirect(url_for('calendar.home'))
    
@calendar.route("/score")
@login_required
def score():
    users = User.query.order_by(User.score.desc()).all()  
    return render_template("score.j2", users=users)

@calendar.route("/answers")
@login_required
def answers():
    if not current_user.is_admin:
        abort(403)
    return render_template("answers.j2")

@calendar.route("/answers/<int:day>")
@login_required
def answers_by_day(day):
    if not current_user.is_admin:
        abort(403) 
    question = Question.query.filter_by(day=day).first_or_404()
    answers = question.answers
    userids_to_users = {}
    users = User.query.all()
    for user in users:
        userids_to_users[user.id] = user.username
    return render_template("answers_by_day.j2", answers=answers, userids_to_users=userids_to_users, day=day)