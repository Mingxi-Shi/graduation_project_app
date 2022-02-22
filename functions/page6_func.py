
import streamlit as st

import time
import base64
from faker import Faker
import pandas as pd


# ------------------Page6:faker data generate假数据生成--------------------
timestr = time.strftime("%Y%m%d-%H%M%S")

# Fxn to Download
def make_downloadable_df(data):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()  # B64 encoding
    st.markdown("### ** Download CSV File ** ")
    new_filename = "fake_dataset_{}.csv".format(timestr)
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!</a>'
    st.markdown(href, unsafe_allow_html=True)


# Fxn to Download Into A Format
def make_downloadable_df_format(data, format_type="csv"):
    if format_type == "csv":
        datafile = data.to_csv(index=False)
    elif format_type == "json":
        datafile = data.to_json()
    b64 = base64.b64encode(datafile.encode()).decode()  # B64 encoding
    st.markdown("### ** Download File  📩 ** ")
    new_filename = "fake_dataset_{}.{}".format(timestr, format_type)
    href = f'<a href="data:file/{format_type};base64,{b64}" download="{new_filename}">Click Here!</a>'
    st.markdown(href, unsafe_allow_html=True)


# Generate A Simple Profile
def generate_profile(number, random_seed=200):
    fake = Faker()
    Faker.seed(random_seed)
    data = [fake.simple_profile() for i in range(number)]
    df = pd.DataFrame(data)
    return df


# Generate A Customized Profile Per Locality
def generate_locale_profile(number, locale, random_seed=200):
    locale_fake = Faker(locale)
    Faker.seed(random_seed)
    data = [locale_fake.simple_profile() for i in range(number)]
    df = pd.DataFrame(data)
    return df
# -----------------------------------------------------------------------
