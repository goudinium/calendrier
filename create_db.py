from petitcalendrier import app, db, bcrypt
from petitcalendrier.models import User

with app.app_context():
    db.drop_all()
    db.create_all()

    pwd = bcrypt.generate_password_hash("fanfan").decode('utf-8')
    admin = User(username='admin', first_name="François", last_name="Goudineau", password=pwd, is_admin=True)

    db.session.add(admin)
    db.session.commit()

