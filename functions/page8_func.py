
import streamlit as st

import os
import jieba  # jieba 中文分词库
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator  # 词云库
from PIL import Image, ImageEnhance  # 图像处理标准库
import numpy as np


def get_stopwords():
    with open('./datasets/cn_stopwords.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        text_list = text.split(';\n')
        s = set(text_list)
    return s


def remove_stopwords(words):
    return [word for word in words if words not in get_stopwords()]
