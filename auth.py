from functools import wraps

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from utils.database import (
    register_user,
    login_user
)

auth_bp = Blueprint("auth", __name__)


# ==========================================
# Login Required Decorator
# ==========================================
def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return wrapper


# ==========================================
# Register
# ==========================================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:

            flash("Passwords do not match.", "danger")

            return redirect(url_for("auth.register"))

        success = register_user(
            full_name,
            email,
            password
        )

        if success:

            flash(
                "Registration successful. Please login.",
                "success"
            )

            return redirect(url_for("auth.login"))

        flash(
            "Email already exists.",
            "danger"
        )

    return render_template("register.html")


# ==========================================
# Login
# ==========================================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = login_user(
            email,
            password
        )

        if user:

            session["user_id"] = user["id"]
            session["full_name"] = user["full_name"]
            session["email"] = user["email"]

            flash(
                "Login Successful",
                "success"
            )

            return redirect(url_for("dashboard"))

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template("login.html")


# ==========================================
# Logout
# ==========================================
@auth_bp.route("/logout")
@login_required
def logout():

    session.clear()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(url_for("home"))