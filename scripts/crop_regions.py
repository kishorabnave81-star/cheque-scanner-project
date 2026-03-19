import cv2
import os

INPUT_FOLDER = "../processed_images"
OUTPUT_FOLDER = "../cropped_regions"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for file in os.listdir(INPUT_FOLDER):

    if file.endswith(".png"):

        path = os.path.join(INPUT_FOLDER, file)

        print("Processing:", path)

        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)[1]

        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        count = 0

        for c in contours:

            x,y,w,h = cv2.boundingRect(c)

            if w > 120 and h > 40:

                crop = img[y:y+h, x:x+w]

                crop_path = os.path.join(
                    OUTPUT_FOLDER, f"{file}_region_{count}.png"
                )

                cv2.imwrite(crop_path, crop)

                count += 1

        print("Regions saved:", count)

print("Cropping completed")