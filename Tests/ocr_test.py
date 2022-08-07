import cv2
import numpy as np
import pytesseract
import time
import matplotlib.pyplot as plt
import sys

img = cv2.imread('../Exports/test81.tiff')
conv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, conv = cv2.threshold(conv, 200, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(conv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
conv2 = cv2.cvtColor(conv, cv2.COLOR_GRAY2BGR)
bounds = []
for cnt in contours:
    # cv2.drawContours(conv2, [cnt], 0, (255, 0, 0), 3)
    x_min, x_max = sys.maxsize, 0
    y_min, y_max = sys.maxsize, 0
    for coord in cnt[:, 0]:    # 1차원은 모두, 2차원은 0번째 원소만 슬라이싱
        x_min = min(x_min, coord[0])
        x_max = max(x_max, coord[0])
        y_min, y_max = min(y_min, coord[1]), max(y_max, coord[1])

    bounds.append([[x_min, y_min], [x_max, y_max]])

for cd in bounds:
    cv2.rectangle(conv2, cd[0], cd[1], (255, 0, 0), 3)


plt.imshow(conv2)
plt.show()
# cv2.imwrite('test2.tiff', conv2)


d = pytesseract.image_to_data(conv, output_type=pytesseract.Output.DICT, config=r'-l kor --psm 6 ')
print(d.keys())

n_boxes = len(d['text'])
for i in range(n_boxes):
    if 100 > float(d['conf'][i]) > 60:
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        conv2 = cv2.rectangle(conv2, (x, y), (x + w, y + h), (0, 255, 0), 5)
        cv2.imshow('img', conv2)
        print(f"conf: {d['conf'][i]}, x: {x}, y: {y}, width: {w}, height: {h} content: {d['text'][i]}")

cv2.imwrite('test2.tiff', conv2)
cv2.waitKey(0)

'''
h, w, c = img.shape
custom_config = r'-l kor --oem 3 --psm 6'
boxes = pytesseract.image_to_boxes(img, config=custom_config)
for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 5)
'''


'''
custom_config = r'-l kor --oem 3 --psm 6'
ocr = pytesseract.image_to_string(img, config=custom_config)
print(ocr)
'''
