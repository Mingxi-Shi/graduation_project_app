from aip import AipNlp

import streamlit as st

import pyperclip

import math

import matplotlib.pyplot as plt

from PIL import Image  # 图像处理标准库


def load_images(image_name):
    img = Image.open(image_name)
    return st.image(img, width=72)

