import cv2
import numpy as np
import pytesseract


def img_preprocess(img_path):
    img = cv2.imread(img_path)
    conv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, conv = cv2.threshold(conv, 200, 255, cv2.THRESH_OTSU)
    return img, conv


def img_segmentation(conv):
    # 이미지 방향 디텍션 추가
    ocr_config = r'-l kor+eng --psm 6'
    d = pytesseract.image_to_data(conv, output_type=pytesseract.Output.DICT, config=ocr_config)
    return d


def blank_detection(conv):
    contours, hierarchy = cv2.findContours(conv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


def deco_removal(conv):
    pass


def img_parsing(img, conv, d):
    pass
