import cv2
import os

INPUT_FOLDER = "../processed_images"
OUTPUT_FOLDER = "../detected_regions"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for file in os.listdir(INPUT_FOLDER):

    if file.endswith(".png"):

        path = os.path.join(INPUT_FOLDER, file)

        print("Processing:", path)

        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # threshold for text detection
        thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)[1]

        # find contours
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for c in contours:

            x, y, w, h = cv2.boundingRect(c)

            if w > 100 and h > 30:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        output_path = os.path.join(OUTPUT_FOLDER, file)

        cv2.imwrite(output_path, img)

        print("Saved:", output_path)

print("Text region detection complete")