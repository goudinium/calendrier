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
    days = [14, 10, 11, 8, 22, 18, 21, 23, 16, 13, 5, 17, 3, 1, 9, 6, 7, 24, 12, 19, 15, 20, 2, 4]
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
                score+=20 
            else:
                score +=1
            current_user.score = score
            db.session.commit()
            return redirect(url_for("calendar.day", day=day))
        return render_template("todays_gift_without_answer.j2", form=form, challenge=challenge, day=day)
    elif day == today and answer != None:
        return render_template("todays_gift_with_answer.j2", day=day, challenge=challenge, answer=answer)
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
        