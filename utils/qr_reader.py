import json
import cv2


# ======================================================
# Read QR Code using OpenCV
# ======================================================
def read_qr(image_path):
    """
    Reads a QR code from the uploaded certificate.

    Returns:
        dict : Parsed JSON data if QR contains JSON.
        str  : Plain text if QR contains text.
        None : If no QR code is found.
    """

    try:
        # Load image
        image = cv2.imread(image_path)

        if image is None:
            print("QR Reader Error: Unable to load image.")
            return None

        # Create QR detector
        detector = cv2.QRCodeDetector()

        # Detect and decode QR
        qr_text, points, _ = detector.detectAndDecode(image)

        # No QR found
        if not qr_text:
            return None

        # Try parsing JSON
        try:
            return json.loads(qr_text)

        except json.JSONDecodeError:
            return qr_text

    except Exception as e:
        print("QR Reader Error:", e)
        return None


# ======================================================
# Test Function
# ======================================================
if __name__ == "__main__":

    image = "sample_certificate.png"

    data = read_qr(image)

    print(data)