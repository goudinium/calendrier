from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, ValidationError, NumberRange

from petitcalendrier.models import User, Question

class LoginForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi?')
    submit = SubmitField('Connexion')


class AnswerForm(FlaskForm):
    answer = SelectField("🙍 Quelle personne se cache derrière cette image?", choices=[
        ('Agathe', 'Agathe'), ('Alexandra', 'Alexandra'), ('Aziliz', 'Aziliz'),
        ('Béatrice', 'Béatrice'), ('Céline', 'Céline'), ('Clotilde', 'Clotilde'),
        ('Evan', 'Evan'), ('Galatée', 'Galatée'), ('Jacques', 'Jacques'), 
        ('Jean-Louis', 'Jean-Louis'), ('Julie', 'Julie'), ('Julien', 'Julien'),
        ('Laurence', 'Laurence'), ('Lenaïc', 'Lenaïc'), ('Loïc', 'Loïc'),
        ('Loren', 'Loren'), ('Oriane', 'Oriane'), ('Papy', 'Papy'), 
        ('Quentin', 'Quentin'), ('Soraya', 'Soraya'), ('Stéphane', 'Stéphane'), 
        ('Théo', 'Théo'), ('Tiphaine', 'Tiphaine'), ('Tristan', 'Tristan'), 
        ('Valérie', 'Valérie')])
    answer_time = StringField("📅 Quel est le moment caché?")
    answer_place = StringField("🌍 Quel est le lieu caché?")
    answer_color = StringField("🎨 Quelle est la couleur cachée?")
    answer_sound = StringField("🔊 Quel est le bruit caché?")
    answer_object = StringField("💎Quel est l'objet?")
    submit = SubmitField("Valider")

class RegisterForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    first_name = StringField("Prénom", validators=[DataRequired()])
    last_name = StringField("Nom de famille", validators=[DataRequired()])
    password = PasswordField('Mot de passe')
    submit = SubmitField("Go")
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Ce nom d'utilisateur existe déjà")
        
class NewQuestionForm(FlaskForm):
    day = IntegerField("Jour de la question", validators=[DataRequired(), NumberRange(min=1, max=24)])
    answer = SelectField(u"Réponse", choices=[('Tiphaine', 'Tiphaine'), ('Francois', 'François')])
    picture = FileField("Photo associée", validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp']), FileRequired()])
    submit = SubmitField("Ajouter")

    def validate_day(self, day):
        question = Question.query.filter_by(day=day.data).first()
        if question:
            raise ValidationError("Il existe déjà une question pour ce jour")