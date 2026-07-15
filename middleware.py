from flask import request, abort

from detector import (
    detect_sql,
    detect_xss,
    detect_command,
    detect_traversal,
    detect_scanner
)

from logger import log_incident


def detect_attack():

    ip = request.remote_addr or "Unknown"

    user_agent = request.headers.get("User-Agent", "")

    payload = ""

    # Collect everything submitted by the user
    if request.form:
        payload += " ".join(request.form.values())

    if request.args:
        payload += " " + " ".join(request.args.values())

    payload = payload.strip()

    # -----------------------
    # SQL Injection
    # -----------------------
    if detect_sql(payload):

        log_incident(
            incident_type="SQL Injection",
            username=payload,
            ip_address=ip,
            severity="Critical",
            description="SQL Injection blocked",
        )

        abort(403)

    # -----------------------
    # XSS
    # -----------------------
    if detect_xss(payload):

        log_incident(
            incident_type="Cross Site Scripting",
            username=payload,
            ip_address=ip,
            severity="High",
            description="XSS attack blocked",
        )

        abort(403)

    # -----------------------
    # Command Injection
    # -----------------------
    if detect_command(payload):

        log_incident(
            incident_type="Command Injection",
            username=payload,
            ip_address=ip,
            severity="Critical",
            description="Command Injection blocked",
        )

        abort(403)

    # -----------------------
    # Directory Traversal
    # -----------------------
    if detect_traversal(payload):

        log_incident(
            incident_type="Directory Traversal",
            username=payload,
            ip_address=ip,
            severity="High",
            description="Directory Traversal blocked",
        )

        abort(403)

    # -----------------------
    # Scanner Detection
    # -----------------------
    if detect_scanner(user_agent):

        log_incident(
            incident_type="Scanner Detection",
            username="Unknown",
            ip_address=ip,
            severity="Medium",
            description=user_agent,
        )

        abort(403)