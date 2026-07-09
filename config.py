import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    # Read the secret key from the environment on Render.
    # Fall back to a development key when running locally.
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "attendance-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(BASE_DIR, "instance", "attendance.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = True