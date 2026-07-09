from datetime import datetime

from models import LoginLog
from incident_report import create_incident


def check_brute_force(username, ip_address):
    """
    Detect brute-force attack after 5 failed login attempts.
    """

    failed_attempts = LoginLog.query.filter_by(
        username=username,
        status="FAILED"
    ).count()

    if failed_attempts >= 5:

        create_incident(
            incident_type="Brute Force Attack",
            username=username,
            ip_address=ip_address,
            severity="High",
            description=f"{failed_attempts} failed login attempts detected."
        )