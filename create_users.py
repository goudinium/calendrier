from petitcalendrier import create_app, db, bcrypt
from petitcalendrier.models import User
import csv


app = create_app()
with app.app_context():
    with open('Users.csv', 'r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            username = line['Pseudo']
            first = line['Prenom']
            second = line['Nom']
            password = line['Password']
            pwd = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(username=username, first_name=first, last_name=second, password=pwd, is_admin=False)
            db.session.add(user)
            db.session.commit()