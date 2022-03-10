import streamlit as st
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
import pandas as pd
import numpy as np
from io import BytesIO


# 转换格式函数csv
def convert2csv_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('GB2312')


# 转换格式函数xlsx
def convert2excel_df(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data





