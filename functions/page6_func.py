
import streamlit as st

import time
from faker import Faker
import pandas as pd
from io import BytesIO
import random


# ------------------Page6:faker data generate假数据生成--------------------
timestr = time.strftime("%Y%m%d-%H%M%S")


def download_df(df):
    df = df
    col1, col2 = st.columns([1, 2])
    with col1:
        st.download_button(label="Download data as CSV",
                           data=make_downloadable_df_format(df, "csv"),
                           file_name="fake_dataset_{}.csv".format(timestr),
                           mime='text/csv',
                           key='download_as_csv',
                           help='click to download the above data as CSV'
                           )
    with col2:
        st.download_button(label="Download data as XLSX",
                           data=make_downloadable_df_format(df, "xlsx"),
                           file_name="fake_dataset_{}.xlsx".format(timestr),
                           mime='text/xlsx',
                           key='download_as_xlsx',
                           help='click to download the above data as XLSX(one sheet)'
                           )


# Fxn to Download Into A Format
def make_downloadable_df_format(df, format_type):
    if format_type == "csv":
        datafile = df.to_csv(index=False).encode('GB2312')
    elif format_type == "xlsx":
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'})
        worksheet.set_column('A:A', None, format1)
        writer.save()
        datafile = output.getvalue()
    return datafile


@st.cache
# Generate A Profile Per Locality
def generate_profile(number, locale, random_seed=200):
    fake = Faker(locale)
    Faker.seed(random_seed)
    data = [fake.simple_profile() for i in range(number)]
    df = pd.DataFrame(data)
    return df


@st.cache
# Generate A Customized Profile Per Locality
def generate_customized_profile(number, locale, fields, random_seed=200):
    custom_fake = Faker(locale)
    Faker.seed(random_seed)
    data = [custom_fake.profile(fields=fields) for i in range(number)]
    df = pd.DataFrame(data)
    return df


def generate_customized_text(locale, types, number, max_chars):
    random_seed = random.randint(1, 200)
    custom_fake = Faker(locale)
    Faker.seed(random_seed)
    if types == "paragraphs":
        return custom_fake.paragraphs(nb=number)
    elif types == "sentences":
        return custom_fake.sentences(nb=number)
    elif types == "texts":
        return custom_fake.texts(nb_texts=number, max_nb_chars=max_chars)
    elif types == "words":
        return custom_fake.words(nb=number, unique=True)
    # text = lorem.Provider.words(self=faker., nb=3)
    # return text
