import streamlit as st

import pandas as pd
import random
import matplotlib.pyplot as plt
from dateutil.parser import parse
from wordcloud import WordCloud, ImageColorGenerator  # 词云库


# ------------------Page2:数据可视化-------------------------------------
def is_date(test_string, fuzzy=False):
    try:
        parse(test_string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False
# ---------------------------------------------------------------------
