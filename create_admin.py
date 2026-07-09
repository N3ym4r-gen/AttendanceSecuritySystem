from werkzeug.security import generate_password_hash

from app import app
from extensions import db
from models import Admin

with app.app_context():

    existing_admin = Admin.query.filter_by(
        username="admin"
    ).first()

    if existing_admin:

        print("Admin already exists.")

    else:

        admin = Admin(
            username="admin",
            password=generate_password_hash("admin123")
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin Created Successfully")