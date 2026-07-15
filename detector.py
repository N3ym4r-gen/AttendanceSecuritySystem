import re


# -----------------------------
# SQL Injection Detection
# -----------------------------
def detect_sql(text):
    if not text:
        return False

    patterns = [
        r"(\bor\b|\band\b).*=.*",
        r"union\s+select",
        r"select\s+.*from",
        r"insert\s+into",
        r"update\s+.*set",
        r"delete\s+from",
        r"drop\s+table",
        r"--",
        r";",
        r"/\*",
        r"\*/",
        r"'",
        r"\""
    ]

    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


# -----------------------------
# Cross-Site Scripting (XSS)
# -----------------------------
def detect_xss(text):
    if not text:
        return False

    patterns = [
        r"<script.*?>",
        r"</script>",
        r"javascript:",
        r"onerror=",
        r"onload=",
        r"<img",
        r"<iframe",
        r"<svg",
        r"alert\("
    ]

    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


# -----------------------------
# Directory Traversal
# -----------------------------
def detect_traversal(text):
    if not text:
        return False

    patterns = [
        r"\.\./",
        r"\.\.\\",
        r"/etc/passwd",
        r"boot.ini",
        r"windows/system32",
        r"win.ini"
    ]

    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


# -----------------------------
# Command Injection
# -----------------------------
def detect_command(text):
    if not text:
        return False

    patterns = [
        r";",
        r"\|\|",
        r"&&",
        r"\|",
        r"`",
        r"\$\(.*\)",
        r"\bwhoami\b",
        r"\bcat\b",
        r"\bls\b",
        r"\bpwd\b",
        r"\bping\b",
        r"\bwget\b",
        r"\bcurl\b",
        r"\bchmod\b",
        r"\brm\b"
    ]

    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


# -----------------------------
# Scanner Detection
# -----------------------------
def detect_scanner(user_agent):
    if not user_agent:
        return False

    scanners = [
        "sqlmap",
        "nikto",
        "nmap",
        "wpscan",
        "burpsuite",
        "burp",
        "acunetix",
        "nessus",
        "openvas",
        "curl",
        "python-requests"
    ]

    user_agent = user_agent.lower()

    for scanner in scanners:
        if scanner in user_agent:
            return True

    return False