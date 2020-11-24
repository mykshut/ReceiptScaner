import pprint
import pytesseract
from imutils.perspective import four_point_transform
import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv


print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("////////////////////////////////////////////////")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
nameofimage = input(str('Give name of your photo: '))
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("////////////////////////////////////////////////")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# Load image, grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread(f'./images/{nameofimage}')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Find contours and sort for largest contour
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None

for c in cnts:
    # Perform contour approximation
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4:
        displayCnt = approx
        break

# Obtain birds' eye view of image
warped = four_point_transform(image, displayCnt.reshape(4, 2))

cv2.imwrite("warped.png", warped)


def get_text_from_img():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(image, lang='pol')
    # text = text.split(',.')
    text1 = text.split()

    if 'Lidl' in text1:
        print('Your check is from Lidl')
    elif 'Biedronka' in text1:
        print('Your check is from Biedronka')
    elif 'Komunikacja' in text1:
        print('Your check is from Komunikacja Miejska Krakowska')
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("////////////////////////////////////////////////")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        result = text.split("\n")
        del result[1:19]
        del result[1]
        del result[3:-1]
        del result[2:3]
        name = result[0]
        suma = result[1].split('SUMA: ')[1]
        value = suma.split(" ")[0]
        pln = value.split(",")[0]
        pln = float(pln)
        text = pln
        print(" ")
    go = input(str('Y for continue, N for stop: '))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("////////////////////////////////////////////////")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    if go == 'Y':
        with open('data.csv', mode='w', newline='') as grades:
            writer = csv.writer(grades)
            writer.writerow([name, pln])

        plt.style.use('ggplot')
        with open('data.csv', mode='r', newline='') as grades:
            reader = csv.reader(grades)
            for record in reader:
                name, pln = record

        pln = float(pln)

        x = [name, "Lidl"]
        energy = [pln, 24.3]

        x_pos = [i for i, _ in enumerate(x)]

        plt.bar(x_pos, energy, color='green')
        plt.xlabel("Energy Source")
        plt.ylabel("Energy Output (GJ)")
        plt.title("Energy output from various fuel sources")

        plt.xticks(x_pos, x)

        plt.show()
    else:
        print('GoodBy')

get_text_from_img()
