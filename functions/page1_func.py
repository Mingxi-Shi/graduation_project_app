
import streamlit as st

import pandas as pd
import numpy as np
from io import BytesIO


# ------------------Page1:功能0-----------------------------------------
def convert_df_columns_datatype(df, cols, types):
    df_columns_name = df.columns.to_list()
    for i in range(len(cols)):
        if df[cols[i]].dtype == 'object':
            if types[i] == 'int64' or types == 'float64':
                st.write('列 [ ', cols[i], ' ] 不能修改为', types[i], '型')
                df[cols[i]] = df[cols[i]].astype('string')
        else:
            df[cols[i]] = df[cols[i]].astype(types[i])
    return df


def judge_original_datatype(df, i):
    index = 0
    df_columns_name = df.columns.to_list()
    if df[df_columns_name[i]].dtype == 'object':
        index = 0
    elif df[df_columns_name[i]].dtype == 'int64':
        index = 1
    elif df[df_columns_name[i]].dtype == 'float64':
        index = 2
    elif df[df_columns_name[i]].dtype == 'bool':
        index = 3
    return index
# ---------------------------------------------------------------------


# ------------------Page1:功能1-----------------------------------------
def drop_na_any(df):
    df = df.dropna(axis=0, how='any', subset=list(df.keys()))
    return df


def drop_na_all(df):
    df = df.dropna(axis=0, how='all', subset=list(df.keys()))
    return df
# ---------------------------------------------------------------------


# ------------------Page1:功能2-----------------------------------------
def drop_duplicates_first(df):
    df = df.drop_duplicates(subset=list(df.keys()), keep='first')
    return df


def drop_duplicates_last(df):
    df = df.drop_duplicates(subset=list(df.keys()), keep='last')
    return df
# ---------------------------------------------------------------------


# ------------------Page1:功能3-----------------------------------------
def fill_na_bfill(df, selected_columns):
    df[selected_columns] = df[selected_columns].fillna(method='bfill', axis=0).fillna(method='ffill', axis=0)
    return df


def fill_na_ffill(df, selected_columns):
    df[selected_columns] = df[selected_columns].fillna(method='ffill', axis=0).fillna(method='bfill', axis=0)
    return df


def fill_na_specific(df, selected_columns, fill_specific_value):
    df[selected_columns] = df[selected_columns].fillna(value=fill_specific_value)
    return df


def replace_all_all_columns(df, to_replace, value):
    df = df.replace(to_replace, value, inplace=False)
    return df


def replace_all_single_columns(df, col, to_replace, value):
    df[col] = df[col].replace(to_replace, value, inplace=False)
    return df


def replace_part_all_columns(df, to_replace, value):  # 未使用
    df = df.str.replace(to_replace, value)
    return df


def replace_part_single_columns(df, col, to_replace, value):
    df[col] = df[col].str.replace(to_replace, value)
    return df
# ---------------------------------------------------------------------


# ------------------Page1:功能7-----------------------------------------

def search_location_numeric(df, value):
    # col_name, row_index, count
    df_columns_name = df.columns.to_list()
    search_result = [[], [], 0]
    for i in range(0, df.shape[0]):
        for j in range(0, df.shape[1]):
            if df.iloc[i][j] == value:
                search_result[0].append(df_columns_name[j])
                search_result[1].append(i)
                search_result[2] = search_result[2] + 1
    return search_result


def search_location_string(df, value):
    # col_name, row_index, count
    df_columns_name = df.columns.to_list()
    search_result = [[], [], 0]
    for i in range(0, df.shape[0]):
        for j in range(0, df.shape[1]):
            if df.iloc[i][j] == value:
                search_result[0].append(df_columns_name[j])
                search_result[1].append(i)
                search_result[2] = search_result[2] + 1
    return search_result


def search_value_numeric(df, col, row):
    value = df[col][row]
    return value


def search_value_string(df, col, row):  # 未使用
    value = df[col][row]
    return value


def search_location_by_columns(df, cols, values):
    index = []
    for i in range(df.shape[0]):
        count = 0
        for j in range(len(cols)):

            if df[cols[j]].dtype == 'bool':
                if values[j] == 'True' or values[j] == 'true':
                    values[j] = bool(1)
                elif values[j] == 'False' or values[j] == 'false':
                    values[j] = bool(0)

            if df.loc[i][cols[j]] == values[j]:
                count = count + 1

        if count == len(cols):
            index.append(i)
    return index
# -----------------------------------------------------------------------


# ------------------Page1:功能8-----------------------------------------
# 转换格式函数csv
def convert2csv_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('GB2312')


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
# ---------------------------------------------------------------------


