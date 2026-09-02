import os

from flask import (
    Flask,
    render_template,
    request,
    session
)

from werkzeug.utils import secure_filename

from config import Config
from auth import auth_bp, login_required

from utils.database import (
    init_db,
    get_history,
    save_certificate,
    get_dashboard_stats,
    get_user_profile
)

from utils.pdf_converter import pdf_to_image
from utils.ocr import extract_text
from utils.qr_reader import read_qr
from utils.verifier import analyze_certificate


app = Flask(__name__)


# ==========================================
# Load Configuration
# ==========================================
app.config.from_object(Config)


# ==========================================
# Register Authentication Blueprint
# ==========================================
app.register_blueprint(auth_bp)


# ==========================================
# Initialize Database
# ==========================================
init_db()


# ==========================================
# Create Upload Folder
# ==========================================
os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)


# ==========================================
# Home
# ==========================================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# Dashboard
# ==========================================
@app.route("/dashboard")
@login_required
def dashboard():

    stats = get_dashboard_stats(
        session["user_id"]
    )

    return render_template(
        "dashboard.html",
        full_name=session.get("full_name"),
        total=stats["total"],
        genuine=stats["genuine"],
        suspicious=stats["suspicious"],
        fake=stats["fake"]
    )


# ==========================================
# Upload Page
# ==========================================
@app.route("/upload")
@login_required
def upload():

    return render_template(
        "upload.html"
    )


# ==========================================
# History
# ==========================================
@app.route("/history")
@login_required
def history():

    records = get_history(
        session["user_id"]
    )

    return render_template(
        "history.html",
        history=records
    )


# ==========================================
# Profile
# ==========================================
@app.route("/profile")
@login_required
def profile():

    user = get_user_profile(
        session["user_id"]
    )

    stats = get_dashboard_stats(
        session["user_id"]
    )

    return render_template(
        "profile.html",
        full_name=user["full_name"],
        email=user["email"],
        total=stats["total"],
        genuine=stats["genuine"],
        suspicious=stats["suspicious"],
        fake=stats["fake"]
    )


# ==========================================
# Verify Certificate
# ==========================================
@app.route("/verify", methods=["POST"])
@login_required
def verify():

    # ------------------------------------------
    # Check File
    # ------------------------------------------
    if "certificate" not in request.files:
        return "No file uploaded"

    file = request.files["certificate"]

    if file.filename == "":
        return "No file selected"


    # ------------------------------------------
    # Get Extension
    # ------------------------------------------
    original_filename = secure_filename(
        file.filename
    )

    extension = (
        os.path.splitext(original_filename)[1]
        .lower()
        .replace(".", "")
    )


    # ------------------------------------------
    # Check Allowed Extension
    # ------------------------------------------
    if extension not in app.config["ALLOWED_EXTENSIONS"]:
        return "Unsupported file type."


    # ------------------------------------------
    # Save Original File
    # ------------------------------------------
    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        original_filename
    )

    file.save(filepath)


    print("\n======================================")
    print("Uploaded File :", filepath)
    print("File Type     :", extension)
    print("======================================")


    # ------------------------------------------
    # File Used For Verification
    # ------------------------------------------
    verification_filepath = filepath


    # ------------------------------------------
    # Preview Image
    #
    # For PDF:
    # PDF -> PNG/JPG image
    #
    # For normal image:
    # Use original image
    # ------------------------------------------
    preview_filepath = filepath


    # ------------------------------------------
    # Convert PDF
    # ------------------------------------------
    if extension == "pdf":

        try:

            verification_filepath = pdf_to_image(
                filepath
            )

            preview_filepath = verification_filepath

            print("\n========== PDF CONVERSION ==========")
            print(
                "PDF Converted To :",
                verification_filepath
            )
            print("====================================")

        except Exception as e:

            print(
                "PDF Conversion Error:",
                e
            )

            return (
                "Unable to convert PDF to image. "
                "Please check the PDF file."
            )


    # ------------------------------------------
    # Get Preview Filename
    # ------------------------------------------
    preview_filename = os.path.basename(
        preview_filepath
    )


    print("\n========== PREVIEW ==========")
    print(
        "Preview Image :",
        preview_filename
    )
    print("=============================")


    # ------------------------------------------
    # OCR
    # ------------------------------------------
    extracted_text = extract_text(
        verification_filepath
    )


    print("\n========== OCR OUTPUT ==========")
    print(extracted_text)
    print("================================")


    # ------------------------------------------
    # QR
    # ------------------------------------------
    qr_data = read_qr(
        verification_filepath
    )


    print("\n========== QR OUTPUT ==========")
    print(qr_data)
    print("================================")


    # ------------------------------------------
    # AI Verification
    # ------------------------------------------
    status, score, checks, organization = analyze_certificate(
        extracted_text,
        qr_data,
        verification_filepath
    )


    print("\n========== AI RESULT ==========")
    print("Organization :", organization)
    print("Status       :", status)
    print("Score        :", score)
    print("Checks       :", checks)
    print("================================")


    # ------------------------------------------
    # Certificate Details
    # ------------------------------------------
    student_name = "Not Available"
    course = "Not Available"
    issue_date = "Not Available"


    # ------------------------------------------
    # Read QR Details
    # ------------------------------------------
    if qr_data:

        try:

            credential = qr_data.get(
                "credentialSubject",
                {}
            )


            student_name = credential.get(
                "issuedTo",
                "Not Available"
            )


            course = credential.get(
                "event",
                "Not Available"
            )


            issue_date = qr_data.get(
                "issuanceDate",
                "Not Available"
            )


        except Exception as e:

            print(
                "QR Parsing Error:",
                e
            )


    # ------------------------------------------
    # Save History
    # ------------------------------------------
    save_certificate(
        session["user_id"],
        student_name,
        course,
        issue_date,
        status,
        score,
        original_filename
    )


    # ------------------------------------------
    # Result Page
    # ------------------------------------------
    return render_template(
        "result.html",

        # Verification Result
        status=status,
        score=score,
        checks=checks,
        organization=organization,

        # Certificate Details
        student_name=student_name,
        course=course,
        issue_date=issue_date,

        # OCR
        extracted_text=extracted_text,

        # Original Uploaded File
        original_file=original_filename,

        # Image to Display
        uploaded_image=preview_filename
    )


# ==========================================
# Run Application
# ==========================================
if __name__ == "__main__":

    app.run(
        debug=True
    )