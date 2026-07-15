from datetime import datetime

from extensions import db
from models import Incident, BlockedIP


def log_incident(
    incident_type,
    username,
    ip_address,
    severity,
    description
):

    # =============================
    # Save Incident
    # =============================

    incident = Incident(

        incident_no="INC" + datetime.now().strftime("%Y%m%d%H%M%S"),

        incident_type=incident_type,

        username=username,

        ip_address=ip_address,

        severity=severity,

        description=description,

        detected_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        status="Open"

    )

    db.session.add(incident)

    # =============================
    # Track IP Address
    # =============================

    ip = BlockedIP.query.filter_by(
        ip_address=ip_address
    ).first()

    if ip:

        ip.attack_count += 1

        # Automatically block after 5 attacks
        if ip.attack_count >= 5:
            ip.blocked = True

    else:

        ip = BlockedIP(

            ip_address=ip_address,

            attack_count=1,

            blocked=False

        )

        db.session.add(ip)

    db.session.commit()