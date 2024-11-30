from petitcalendrier import create_app, db, bcrypt
from petitcalendrier.models import User, Question
from petitcalendrier import Config
import csv

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    pwd = bcrypt.generate_password_hash(Config.ADMIN_PASSWORD).decode('utf-8')
    admin = User(username='admin', first_name="François", last_name="Goudineau", password=pwd, is_admin=True)

    db.session.add(admin)
    db.session.commit()

    # creating the questions
    with open('questionnaire.csv', 'r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            day = line['jour'].strip()
            image = line['image'].strip()
            answer = line['personne'].strip()
            time = line['periode'].strip()
            object = line['objet'].strip()
            place = line['lieu'].strip()
            sound = line['bruit'].strip()
            color = line['couleur'].strip()
            q = Question(day=day, image=image, answer=answer, solution_time=time, solution_object=object, solution_place=place, solution_sound=sound, solution_color=color)
            db.session.add(q)    
            db.session.commit()
