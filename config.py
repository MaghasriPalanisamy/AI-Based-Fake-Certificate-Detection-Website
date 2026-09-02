import os


class Config:

    # Flask Secret Key
    SECRET_KEY = "certiguard_secret_key"

    # Database
    DATABASE = "database.db"

    # Upload Folder
    UPLOAD_FOLDER = os.path.join(
        "static",
        "uploads"
    )

    # Allowed Extensions
    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "pdf",
        "webp",
        "bmp",
        "tiff"
    }

    # Reference Folder
    REFERENCE_FOLDER = os.path.join(
        "static",
        "reference"
    )

    # Maximum Upload Size (20 MB)
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024