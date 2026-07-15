from flask import (
    request,
    render_template,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from datetime import datetime

from app import app
from extensions import db

from forms import (
    StudentForm,
    LoginForm,
    AdminLoginForm
)

from models import (
    Student,
    Attendance,
    Admin,
    LoginLog,
    Incident
)
from detector import detect_sql
from logger import log_incident

from security_engine import check_brute_force

# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# STUDENT REGISTRATION
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    form = StudentForm()

    if form.validate_on_submit():

        if Student.query.filter_by(email=form.email.data).first():
            flash("Email already exists!", "danger")
            return render_template("register.html", form=form)

        if Student.query.filter_by(matric_no=form.matric_no.data).first():
            flash("Matric Number already exists!", "danger")
            return render_template("register.html", form=form)

        student = Student(
            fullname=form.fullname.data,
            matric_no=form.matric_no.data,
            department=form.department.data,
            level=form.level.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )

        db.session.add(student)
        db.session.commit()

        flash("Registration Successful!", "success")

        return redirect(url_for("register"))

    return render_template("register.html", form=form)


# ==========================================
# STUDENT LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        student = Student.query.filter_by(
            matric_no=form.matric_no.data
        ).first()

        ip = request.remote_addr

        if student and check_password_hash(
            student.password,
            form.password.data
        ):

            log = LoginLog(
                username=form.matric_no.data,
                ip_address=ip,
                login_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status="SUCCESS"
            )

            db.session.add(log)
            db.session.commit()

            session.clear()
            session["student_id"] = student.id

            flash("Login Successful!", "success")

            return redirect(url_for("dashboard"))

    
        log = LoginLog(
            username=form.matric_no.data,
            ip_address=ip,
            login_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status="FAILED"
        )

        db.session.add(log)
        db.session.commit()

        # Check for brute-force attack
        check_brute_force(
            username=form.matric_no.data,
            ip_address=ip
        )

        flash("Invalid Matric Number or Password!", "danger")

    return render_template(
        "login.html",
        form=form
    )

# ==========================================
# STUDENT DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    if "student_id" not in session:
        return redirect(url_for("login"))

    student = Student.query.get(session["student_id"])

    attendance = Attendance.query.filter_by(
        student_id=student.id
    ).order_by(
        Attendance.id.desc()
    ).all()

    present_days = Attendance.query.filter_by(
        student_id=student.id,
        status="Present"
    ).count()

    late_days = Attendance.query.filter_by(
        student_id=student.id,
        status="Late"
    ).count()

    total_days = Attendance.query.filter_by(
        student_id=student.id
    ).count()

    return render_template(
        "dashboard.html",
        student=student,
        attendance=attendance,
        present_days=present_days,
        late_days=late_days,
        total_days=total_days
    )


# ==========================================
# SIGN IN
# ==========================================

@app.route("/signin")
def signin():

    if "student_id" not in session:
        return redirect(url_for("login"))

    today = datetime.now().strftime("%Y-%m-%d")

    record = Attendance.query.filter_by(
        student_id=session["student_id"],
        date=today
    ).first()

    if record:
        flash("You have already signed in today.", "warning")
        return redirect(url_for("dashboard"))

    now = datetime.now()

    sign_in_time = now.strftime("%H:%M:%S")

    late_time = datetime.strptime(
        "08:00:00",
        "%H:%M:%S"
    ).time()

    status = "Present"

    if now.time() > late_time:
        status = "Late"

    attendance = Attendance(
        student_id=session["student_id"],
        date=today,
        sign_in=sign_in_time,
        status=status
    )

    db.session.add(attendance)
    db.session.commit()

    flash(f"Sign In Successful! Status: {status}", "success")

    return redirect(url_for("dashboard"))


# ==========================================
# SIGN OUT
# ==========================================

@app.route("/signout")
def signout():

    if "student_id" not in session:
        return redirect(url_for("login"))

    today = datetime.now().strftime("%Y-%m-%d")

    record = Attendance.query.filter_by(
        student_id=session["student_id"],
        date=today
    ).first()

    if not record:
        flash("Please sign in first.", "danger")
        return redirect(url_for("dashboard"))

    if record.sign_out:
        flash("You have already signed out today.", "warning")
        return redirect(url_for("dashboard"))

    record.sign_out = datetime.now().strftime("%H:%M:%S")

    db.session.commit()

    flash("Sign Out Successful!", "success")

    return redirect(url_for("dashboard"))


# ==========================================
# STUDENT LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully!", "success")

    return redirect(url_for("login"))


# ==========================================
# ADMIN LOGIN
# ==========================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    form = AdminLoginForm()

    if form.validate_on_submit():

        admin = Admin.query.filter_by(
            username=form.username.data
        ).first()

        if admin and check_password_hash(
            admin.password,
            form.password.data
        ):

            session.clear()

            session["admin_id"] = admin.id

            flash("Administrator Login Successful!", "success")

            return redirect(url_for("admin_dashboard"))

        flash("Invalid Administrator Login!", "danger")

    return render_template(
        "admin_login.html",
        form=form
    )


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    today = datetime.now().strftime("%Y-%m-%d")

    # -------------------------
    # Attendance Statistics
    # -------------------------
    total_students = Student.query.count()

    present_today = Attendance.query.filter_by(
        date=today,
        status="Present"
    ).count()

    late_today = Attendance.query.filter_by(
        date=today,
        status="Late"
    ).count()

    attendance = Attendance.query.order_by(
        Attendance.id.desc()
    ).all()

    # -------------------------
    # Security Statistics
    # -------------------------
    total_incidents = Incident.query.count()

    open_incidents = Incident.query.filter_by(
        status="Open"
    ).count()

    sql_injections = Incident.query.filter_by(
        incident_type="SQL Injection"
    ).count()

    xss_attacks = Incident.query.filter_by(
        incident_type="Cross Site Scripting"
    ).count()

    command_injections = Incident.query.filter_by(
        incident_type="Command Injection"
    ).count()

    directory_traversals = Incident.query.filter_by(
        incident_type="Directory Traversal"
    ).count()

    scanners = Incident.query.filter_by(
        incident_type="Scanner Detection"
    ).count()

    recent_incidents = Incident.query.order_by(
        Incident.id.desc()
    ).limit(10).all()

    return render_template(
        "admin_dashboard.html",
        total_students=total_students,
        present_today=present_today,
        late_today=late_today,
        attendance=attendance,

        total_incidents=total_incidents,
        open_incidents=open_incidents,
        sql_injections=sql_injections,
        xss_attacks=xss_attacks,
        command_injections=command_injections,
        directory_traversals=directory_traversals,
        scanners=scanners,
        recent_incidents=recent_incidents
    )

# ==========================================
# INCIDENT DASHBOARD
# ==========================================

@app.route("/admin/incidents")
def incident_dashboard():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    incidents = Incident.query.order_by(
        Incident.id.desc()
    ).all()

    total_incidents = Incident.query.count()

    open_incidents = Incident.query.filter_by(
        status="Open"
    ).count()

    closed_incidents = Incident.query.filter_by(
        status="Closed"
    ).count()

    high_incidents = Incident.query.filter_by(
        severity="High"
    ).count()

    return render_template(
        "incident_dashboard.html",
        incidents=incidents,
        total_incidents=total_incidents,
        open_incidents=open_incidents,
        closed_incidents=closed_incidents,
        high_incidents=high_incidents
    )

# ==========================================
# CLOSE INCIDENT
# ==========================================

@app.route("/incident/close/<int:id>")
def close_incident(id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    incident = Incident.query.get_or_404(id)

    incident.status = "Closed"

    db.session.commit()

    flash("Incident Closed Successfully!", "success")

    return redirect(url_for("incident_dashboard"))

# ==========================================
# SECURITY LOGS
# ==========================================

@app.route("/security/logs")
def security_logs():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    logs = LoginLog.query.order_by(
        LoginLog.id.desc()
    ).all()

    return render_template(
        "security_logs.html",
        logs=logs
    )


# ==========================================
# ADMIN LOGOUT
# ==========================================

@app.route("/admin/logout")
def admin_logout():

    session.clear()

    flash("Administrator Logged Out!", "success")

    return redirect(url_for("admin_login"))

@app.errorhandler(403)
def forbidden(error):

    return render_template("403.html"), 403