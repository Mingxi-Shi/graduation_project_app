
import streamlit as st

import cv2
import numpy as np
from PIL import Image, ImageEnhance  # 图像处理标准库


# ------------------Page7:face detection人脸检测---------------------------
def detect_faces(original_image):
    face_cascade = cv2.CascadeClassifier('resources/frecog/haarcascade_frontalface_default.xml')

    rgb_array_img = np.array(original_image.convert('RGB'))
    img = cv2.cvtColor(rgb_array_img, 1)
    gray = cv2.cvtColor(rgb_array_img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return img, faces


def detect_smiles(original_image):
    smile_cascade = cv2.CascadeClassifier('resources/frecog/haarcascade_smile.xml')

    rgb_array_img = np.array(original_image.convert('RGB'))
    img = cv2.cvtColor(rgb_array_img, 1)
    gray = cv2.cvtColor(rgb_array_img, cv2.COLOR_BGR2GRAY)
    # Detect Smiles
    smiles = smile_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw rectangle around the Smiles
    for (x, y, w, h) in smiles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return img


def detect_eyes(original_image):
    eye_cascade = cv2.CascadeClassifier('resources/frecog/haarcascade_eye.xml')

    rgb_array_img = np.array(original_image.convert('RGB'))
    img = cv2.cvtColor(rgb_array_img, 1)
    gray = cv2.cvtColor(rgb_array_img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    return img


def cannize_image(original_image):
    rgb_array_img = np.array(original_image.convert('RGB'))
    img = cv2.cvtColor(rgb_array_img, 1)
    img = cv2.GaussianBlur(img, (11, 11), 0)
    canny = cv2.Canny(img, 100, 150)
    return canny


def cartonize_image(original_image):
    rgb_array_img = np.array(original_image.convert('RGB'))
    img = cv2.cvtColor(rgb_array_img, 1)
    gray = cv2.cvtColor(rgb_array_img, cv2.COLOR_BGR2GRAY)
    # Edges
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    # Color
    color = cv2.bilateralFilter(img, 9, 300, 300)
    # Cartoon
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

# -----------------------------------------------------------------------
