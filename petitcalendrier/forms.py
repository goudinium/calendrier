from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError

from petitcalendrier.models import User


class LoginForm(FlaskForm):
    username = StringField('Nom', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi?')
    submit = SubmitField('Connexion')

class RegisterForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired()])
    first_name = StringField("Prénom", validators=[DataRequired()])
    last_name = StringField("Nom de famille", validators=[DataRequired()])
    password = PasswordField('Mot de passe')
    submit = SubmitField("Créer")
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Ce nom d'utilisateur existe déjà")