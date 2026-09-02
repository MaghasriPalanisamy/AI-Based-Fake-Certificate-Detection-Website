import re

from utils.signature_detector import detect_signature


def analyze_certificate(extracted_text, qr_data, image_path):

    score = 0
    checks = []

    text = extracted_text.upper()

    # ==========================================
    # 1. QR Verification (30 Marks)
    # ==========================================
    if qr_data:
        score += 30
        checks.append(("QR Verification", True, 30))
    else:
        checks.append(("QR Verification", False, 0))

    # ==========================================
    # 2. Certificate ID Verification (25 Marks)
    # ==========================================
    cert_patterns = [
        r"CERT[- ]?\d+",
        r"CERTIFICATE\s*ID[: ]*[A-Z0-9-]+",
        r"ID[: ]*[A-Z0-9-]+",
        r"REGISTRATION\s*NO[: ]*[A-Z0-9-]+",
        r"VERIFY[: ]*[A-Z0-9-]+"
    ]

    certificate_found = False

    for pattern in cert_patterns:
        if re.search(pattern, text):
            certificate_found = True
            break

    if certificate_found:
        score += 25
        checks.append(("Certificate ID Verification", True, 25))
    else:
        checks.append(("Certificate ID Verification", False, 0))

    # ==========================================
    # 3. OCR Verification (20 Marks)
    # ==========================================
    keywords = [
        "CERTIFICATE",
        "NAME",
        "COURSE",
        "DATE",
        "ISSUED",
        "COMPLETION",
        "SUCCESSFULLY",
        "AWARDED",
        "VERIFY"
    ]

    matched = 0

    for keyword in keywords:
        if keyword in text:
            matched += 1

    ocr_marks = int((matched / len(keywords)) * 20)

    score += ocr_marks

    checks.append((
        "OCR Verification",
        matched >= 4,
        ocr_marks
    ))

    # ==========================================
    # 4. Organization Detection (20 Marks)
    # ==========================================

    organizations = {
        "INFOSYS": "Infosys",
        "IBM": "IBM",
        "MICROSOFT": "Microsoft",
        "NPTEL": "NPTEL",
        "COURSERA": "Coursera",
        "AWS": "AWS",
        "GOOGLE": "Google",
        "ORACLE": "Oracle",
        "CISCO": "Cisco",
        "UDEMY": "Udemy"
    }

    organization = "Unknown"

    for key, value in organizations.items():

        if key in text:

            organization = value
            score += 20

            checks.append((
                "Organization Detection",
                True,
                20
            ))

            break

    if organization == "Unknown":

        checks.append((
            "Organization Detection",
            False,
            0
        ))

    # ==========================================
    # 5. Signature Detection (5 Marks)
    # ==========================================

    signature_found = detect_signature(image_path)

    if signature_found:

        score += 5

        checks.append((
            "Signature Detection",
            True,
            5
        ))

    else:

        checks.append((
            "Signature Detection",
            False,
            0
        ))

    # ==========================================
    # Final Score
    # ==========================================

    if score > 100:
        score = 100

    percentage = score

    # ==========================================
    # Final Status
    # ==========================================

    if percentage >= 90:
        status = "🟢 Genuine"

    elif percentage >= 70:
        status = "🟡 Probably Genuine"

    elif percentage >= 50:
        status = "🟠 Suspicious"

    else:
        status = "🔴 Fake"

    return status, percentage, checks, organization