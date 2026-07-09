from app import app
from extensions import db
import models

with app.app_context():
    db.create_all()
    print("Database and tables created successfully!")