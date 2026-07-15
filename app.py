from flask import Flask
from config import Config
from extensions import db
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# ===========================
# Import models
# ===========================
import models
from models import Admin

# ===========================
# Import security middleware
# ===========================
from middleware import detect_attack

# Inspect every incoming request
@app.before_request
def before_request():
    detect_attack()

# ===========================
# Import routes
# ===========================
from routes import *

# ===========================
# Create database tables
# ===========================
with app.app_context():

    db.create_all()

    # Create default administrator
    if not Admin.query.filter_by(username="admin").first():

        admin = Admin(
            username="admin",
            password=generate_password_hash("admin123")
        )

        db.session.add(admin)
        db.session.commit()

        print("✓ Default administrator account created.")

    else:

        print("✓ Administrator account already exists.")

# ===========================
# Run application
# ===========================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )