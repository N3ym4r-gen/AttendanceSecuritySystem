from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class StudentForm(FlaskForm):

    fullname = StringField("Full Name", validators=[DataRequired()])

    matric_no = StringField("Matric Number", validators=[DataRequired()])

    department = StringField("Department", validators=[DataRequired()])

    level = StringField("Level", validators=[DataRequired()])

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Register Student")


class LoginForm(FlaskForm):

    matric_no = StringField(
        "Matric Number",
        validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Student Login")


class AdminLoginForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Admin Login")