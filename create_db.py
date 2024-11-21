from petitcalendrier import app, db, bcrypt
from petitcalendrier.models import User, Question

with app.app_context():
    db.drop_all()
    db.create_all()

    pwd = bcrypt.generate_password_hash("fanfan").decode('utf-8')
    admin = User(username='admin', first_name="François", last_name="Goudineau", password=pwd, is_admin=True)

    db.session.add(admin)
    db.session.commit()

    for i in range(1, 25):
        question = Question(day=i, image="singe.png", answer="Tiphaine", solution_time='mai', solution_place='brochant',
                            solution_object='mp3', solution_sound='métro', solution_color="bleu")
        db.session.add(question)    
        db.session.commit()