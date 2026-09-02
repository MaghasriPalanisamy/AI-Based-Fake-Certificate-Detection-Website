import pytesseract
import cv2
import os

# ======================================================
# Configure Tesseract
# ======================================================

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

print("Tesseract Exists:", os.path.exists(TESSERACT_PATH))

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


# ======================================================
# Image Preprocessing
# ======================================================

def preprocess_image(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Increase image size (improves OCR)
    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    # Remove noise
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Adaptive threshold
    gray = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    return gray


# ======================================================
# OCR Extraction
# ======================================================

def extract_text(image_path):

    try:

        processed = preprocess_image(image_path)

        # Tesseract Configuration
        custom_config = r'--oem 3 --psm 6'

        text = pytesseract.image_to_string(
            processed,
            lang="eng",
            config=custom_config
        )

        print("\n========== OCR OUTPUT ==========")
        print(text)
        print("================================")

        return text.strip()

    except Exception as e:

        print("OCR Error:", e)

        return ""


# ======================================================
# Test
# ======================================================

if __name__ == "__main__":

    image = "sample.png"

    text = extract_text(image)

    print(text)