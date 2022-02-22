
import streamlit as st

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

import emoji
import pandas as pd

from textblob import TextBlob
from snownlp import SnowNLP
from aip import AipNlp

# ----------------------Page12:情感分析-----------------------------------
# Fetch Text From Url
@st.cache
def get_text(raw_url):
    page = urlopen(raw_url)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text
# -----------------------------------------------------------------------

