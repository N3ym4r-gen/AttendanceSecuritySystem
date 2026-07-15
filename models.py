from extensions import db


class Student(db.Model):

    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100), nullable=False)

    matric_no = db.Column(db.String(30), unique=True, nullable=False)

    department = db.Column(db.String(100))

    level = db.Column(db.String(20))

    email = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(200))


class Attendance(db.Model):

    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    date = db.Column(db.String(20))

    sign_in = db.Column(db.String(20))

    sign_out = db.Column(db.String(20))

    status = db.Column(db.String(20))

    student = db.relationship(
        "Student",
        backref="attendance_records"
    )


class Admin(db.Model):

    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True)

    password = db.Column(db.String(200))


class LoginLog(db.Model):

    __tablename__ = "login_log"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))

    ip_address = db.Column(db.String(100))

    login_time = db.Column(db.String(100))

    status = db.Column(db.String(20))


class Incident(db.Model):

    __tablename__ = "incident"

    id = db.Column(db.Integer, primary_key=True)

    incident_no = db.Column(db.String(30), unique=True)

    incident_type = db.Column(db.String(100))

    username = db.Column(db.String(100))

    ip_address = db.Column(db.String(100))

    severity = db.Column(db.String(20))

    description = db.Column(db.String(300))

    detected_time = db.Column(db.String(100))

    status = db.Column(db.String(30))
    
class BlockedIP(db.Model):

    __tablename__ = "blocked_ip"

    id = db.Column(db.Integer, primary_key=True)

    ip_address = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    attack_count = db.Column(
        db.Integer,
        default=1
    )

    blocked = db.Column(
        db.Boolean,
        default=False
    )