import cv2
import os

INPUT_FOLDER = "../output"
OUTPUT_FOLDER = "../processed_images"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for file in os.listdir(INPUT_FOLDER):
    if file.endswith(".png"):

        img_path = os.path.join(INPUT_FOLDER, file)

        print("Processing:", img_path)

        img = cv2.imread(img_path)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Increase contrast using CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        contrast = clahe.apply(gray)

        # Light Gaussian blur
        blur = cv2.GaussianBlur(contrast, (3,3), 0)

        # Resize image
        resized = cv2.resize(blur, None, fx=1.5, fy=1.5)

        output_path = os.path.join(OUTPUT_FOLDER, file)

        cv2.imwrite(output_path, resized)

        print("Saved:", output_path)

print("Image preprocessing completed")