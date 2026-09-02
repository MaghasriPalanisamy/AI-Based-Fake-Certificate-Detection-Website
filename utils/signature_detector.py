import cv2


def detect_signature(image_path):
    """
    Detect whether a signature exists in the lower-right
    region of the certificate.
    """

    try:

        image = cv2.imread(image_path)

        if image is None:
            return False

        height, width = image.shape[:2]

        # Bottom-right area (typical signature location)
        roi = image[
            int(height * 0.70):height,
            int(width * 0.60):width
        ]

        gray = cv2.cvtColor(
            roi,
            cv2.COLOR_BGR2GRAY
        )

        _, thresh = cv2.threshold(
            gray,
            180,
            255,
            cv2.THRESH_BINARY_INV
        )

        contours, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        area = 0

        for cnt in contours:
            area += cv2.contourArea(cnt)

        if area > 1500:
            return True

        return False

    except Exception as e:

        print("Signature Detection Error:", e)

        return False