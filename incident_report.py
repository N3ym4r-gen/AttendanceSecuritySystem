from datetime import datetime

from extensions import db
from models import Incident


def create_incident(
    incident_type,
    username,
    ip_address,
    severity,
    description
):
    """
    Create a new cybersecurity incident.
    Prevent duplicate OPEN incidents for the same user and type.
    """

    # Check if an open incident already exists
    existing = Incident.query.filter_by(
        incident_type=incident_type,
        username=username,
        status="Open"
    ).first()

    if existing:
        return

    # Generate Incident Number
    total = Incident.query.count() + 1

    incident_number = f"INC-{total:06d}"

    incident = Incident(
        incident_no=incident_number,
        incident_type=incident_type,
        username=username,
        ip_address=ip_address,
        severity=severity,
        description=description,
        detected_time=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        status="Open"
    )

    db.session.add(incident)
    db.session.commit()