import cv2
import numpy as np


# ======================================================
# Resize Image
# ======================================================
def resize_image(image, width=1200):

    h, w = image.shape[:2]

    if w > width:

        ratio = width / float(w)

        height = int(h * ratio)

        image = cv2.resize(
            image,
            (width, height),
            interpolation=cv2.INTER_AREA
        )

    return image


# ======================================================
# Convert to Grayscale
# ======================================================
def to_grayscale(image):

    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


# ======================================================
# Remove Noise
# ======================================================
def remove_noise(image):

    return cv2.medianBlur(
        image,
        3
    )


# ======================================================
# Increase Contrast
# ======================================================
def increase_contrast(image):

    return cv2.equalizeHist(image)


# ======================================================
# Sharpen Image
# ======================================================
def sharpen(image):

    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    return cv2.filter2D(
        image,
        -1,
        kernel
    )


# ======================================================
# Threshold Image
# ======================================================
def threshold(image):

    _, thresh = cv2.threshold(
        image,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresh


# ======================================================
# Complete Preprocessing
# ======================================================
def preprocess_image(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(
            f"Cannot read image: {image_path}"
        )

    image = resize_image(image)

    gray = to_grayscale(image)

    gray = remove_noise(gray)

    gray = increase_contrast(gray)

    gray = sharpen(gray)

    processed = threshold(gray)

    return processed


# ======================================================
# Save Processed Image
# ======================================================
def save_processed(image, output_path):

    cv2.imwrite(
        output_path,
        image
    )


# ======================================================
# Test
# ======================================================
if __name__ == "__main__":

    image_path = "sample.jpg"

    processed = preprocess_image(image_path)

    save_processed(
        processed,
        "processed_sample.png"
    )

    print("Image preprocessing completed.")