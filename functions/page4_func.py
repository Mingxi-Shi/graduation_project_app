
import streamlit as st

from PIL import Image, ImageEnhance  # 图像处理标准库
import gender_ai as ga


# ------------------Page4:gender classifier性别识别------------------------
def load_images(image_name):
    img = Image.open(image_name)
    return st.image(img, width=300)
# -----------------------------------------------------------------------
