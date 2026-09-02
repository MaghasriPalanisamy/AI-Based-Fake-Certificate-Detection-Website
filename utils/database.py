import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "database.db"


# ==========================================
# Database Connection
# ==========================================
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# Initialize Database
# ==========================================
def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Verification History
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            student_name TEXT,
            course TEXT,
            issue_date TEXT,
            status TEXT,
            score INTEGER,
            filename TEXT,
            verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ==========================================
# Register User
# ==========================================
def register_user(full_name, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        password_hash = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO users
            (full_name, email, password)
            VALUES (?, ?, ?)
        """, (
            full_name,
            email,
            password_hash
        ))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# ==========================================
# Login User
# ==========================================
def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE email=?
    """, (email,))

    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user["password"], password):
        return dict(user)

    return None


# ==========================================
# Save Verification
# ==========================================
def save_certificate(
    user_id,
    student_name,
    course,
    issue_date,
    status,
    score,
    filename
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO history(
            user_id,
            student_name,
            course,
            issue_date,
            status,
            score,
            filename
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        student_name,
        course,
        issue_date,
        status,
        score,
        filename
    ))

    conn.commit()
    conn.close()


# ==========================================
# Get Verification History
# ==========================================
def get_history(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM history
        WHERE user_id=?
        ORDER BY verified_at DESC
    """, (user_id,))

    history = cursor.fetchall()

    conn.close()

    return history


# ==========================================
# Dashboard Statistics
# ==========================================
def get_dashboard_stats(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM history
        WHERE user_id=?
    """, (user_id,))
    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(*) AS genuine
        FROM history
        WHERE user_id=?
        AND status LIKE '%Genuine%'
    """, (user_id,))
    genuine = cursor.fetchone()["genuine"]

    cursor.execute("""
        SELECT COUNT(*) AS suspicious
        FROM history
        WHERE user_id=?
        AND status LIKE '%Suspicious%'
    """, (user_id,))
    suspicious = cursor.fetchone()["suspicious"]

    cursor.execute("""
        SELECT COUNT(*) AS fake
        FROM history
        WHERE user_id=?
        AND status LIKE '%Fake%'
    """, (user_id,))
    fake = cursor.fetchone()["fake"]

    conn.close()

    return {
        "total": total,
        "genuine": genuine,
        "suspicious": suspicious,
        "fake": fake
    }


# ==========================================
# Get User Profile
# ==========================================
def get_user_profile(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE id=?
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    if user:
        return dict(user)

    return None