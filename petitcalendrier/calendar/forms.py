from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class AnswerForm(FlaskForm):
    answer_character = SelectField("🙍 Quelle personne se cache derrière cette image?", choices=[
        ('Agathe', 'Agathe'), ('Alexandra', 'Alexandra'), ('Aziliz', 'Aziliz'),
        ('Beatrice', 'Béatrice'), ('Celine', 'Céline'), ('Clotilde', 'Clotilde'),
        ('Evan', 'Evan'), ('Galatee', 'Galatée'), ('Jacques', 'Jacques'), 
        ('Jean-Louis', 'Jean-Louis'), ('Julie', 'Julie'), ('Julien', 'Julien'),
        ('Laurence', 'Laurence'), ('Lenaic', 'Lenaïc'), ('Loic', 'Loïc'),
        ('Loren', 'Loren'), ('Oriane', 'Oriane'), ('Papy', 'Papy'), 
        ('Quentin', 'Quentin'), ('Soraya', 'Soraya'), ('Stephane', 'Stéphane'), 
        ('Theophile', 'Théophile'), ('Tiphaine', 'Tiphaine'), ('Tristan', 'Tristan'), 
        ('Valerie', 'Valérie')], validators=[DataRequired(True)])
    answer_time = StringField("📅 Quel est le moment caché?", validators=[DataRequired(), Length(min=1, max=60, message="Réponse trop longue/vide")])
    answer_place = StringField("🌍 Quel est le lieu caché?", validators=[DataRequired(), Length(min=1, max=60, message="Réponse trop longue/vide")])
    answer_color = StringField("🎨 Quelle est la couleur cachée?", validators=[DataRequired(), Length(min=1, max=60, message="Réponse trop longue/vide")])
    answer_sound = StringField("🔊 Quel est le bruit caché?", validators=[DataRequired(), Length(min=1, max=60, message="Réponse trop longue/vide")])
    answer_object = StringField("💎Quel est l'objet vintage caché?", validators=[DataRequired(), Length(min=1, max=60, message="Réponse trop longue/vide")])
    submit = SubmitField("Valider")

