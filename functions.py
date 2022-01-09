# done by Muench
# Creation Date: 2021/12/10 14:04
# -*- coding:utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_string_dtype
import xlsxwriter
# 全局变量
# df = pd.DataFrame()


# 数据处理
def page1():
    # global df
    st.write("This is page1")
    data = st.file_uploader("上传数据", type=["csv", 'txt', 'xlsx', 'xls'])
    if data is not None:
        # if data.type == "application/vnd.ms-excel":
        if data.name[-3:] == "csv" or data.name[-3:] == "txt":
            # st.write("This is csv")
            df = pd.read_csv(data)
            if st.checkbox("Show All data"):  # 默认显示前20行，选中即显示全部数据
                st.dataframe(df)
            else:
                st.dataframe(df.head(20))

        # elif data.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        elif data.name[-3:] == "xls" or data.name[-4:] == "xlsx":
            # st.write("This is excel")
            df = pd.read_excel(data)
            if st.checkbox("Show All data"):  # 默认显示前20行，选中即显示全部数据
                st.dataframe(df)
            else:
                st.dataframe(df.head(20))

        st.write("每个功能模块都在container内")
        # 功能0：修改列数据类型
        with st.expander(label="功能0：修改数据类型", expanded=False):
            with st.container():
                df_columns_name = df.columns.to_list()
                modified_datatype = [' ' for _ in range(len(df.columns))]
                p1, p2 = st.columns([1, 5])
                with p1:
                    for i in range(len(df_columns_name)):
                        modified_datatype[i] = st.selectbox(label='选择列 [ '+df_columns_name[i]+' ]的数据类型',
                                                            options=['string', 'int64', 'float64', 'bool'], key=i,
                                                            index=judge_original_datatype(df, i))
                    temp = convert_df_columns_datatype(df, df_columns_name, modified_datatype)
                    if st.button("确认修改", key='modify_datatype'):
                        st.write('success')
                        df = temp

                with p2:
                    st.text('')
                    st.text('')
                    st.write(df.head(20))

        # 功能1：数据去空（不同条件）
        with st.expander(label="功能1：数据去空（不同条件）", expanded=False):
            with st.container():
                drop_na_row = st.radio(label="选择你要去空的方式", options=('去空(by row & any)', '去空(by row & all)'))
                if drop_na_row == '去空(by row & any)':
                    temp_na = drop_na_any(df)
                    st.write(temp_na)
                elif drop_na_row == '去空(by row & all)':
                    temp_na = drop_na_all(df)
                    st.write(temp_na)

                if st.button("确认去空"):
                    df = temp_na
                    st.write(df)

        # 功能2：数据去重（不同条件）
        with st.expander(label="功能2：数据去重（不同条件）", expanded=False):
            with st.container():
                drop_duplicates = st.radio(label="选择你要去重的方式", options=('去重(first)', '去重(last)'))
                if drop_duplicates == '去重(first)':
                    temp_duplicates = drop_duplicates_first(df)
                    st.write(temp_duplicates)
                elif drop_duplicates == '去重(last)':
                    temp_duplicates = drop_duplicates_last(df)
                    st.write(temp_duplicates)

                if st.button("确认去重"):
                    df = temp_duplicates
                    st.write(df)

        # 功能3：空值填充和批量替换
        with st.expander(label="功能3：空值填充和批量替换", expanded=False):
            with st.container():
                process_way = st.radio(label="选择你进行的操作", options=('空值填充', '批量替换'))
                df_columns_name = df.columns.to_list()
                if process_way == '空值填充':
                    selected_fill_columns_name = st.multiselect(label='选择你要空值填充的列(可多选)', options=df_columns_name)
                    fill_na_way = st.radio(label="选择填充空值的方式", options=('向前填充(bfill)', '向后填充(ffill)', '填充指定的值'))
                    if fill_na_way == '向前填充(bfill)':
                        temp_filled = fill_na_bfill(df[selected_fill_columns_name])
                        if len(selected_fill_columns_name) != 0:
                            st.write(temp_filled)
                    elif fill_na_way == '向后填充(ffill)':
                        temp_filled = fill_na_ffill(df[selected_fill_columns_name])
                        if len(selected_fill_columns_name) != 0:
                            st.write(temp_filled)
                    elif fill_na_way == '填充指定的值':
                        fill_specific_value = st.text_input(label='输入你要填充的值', placeholder=0)
                        # st.write(fill_specific_value)
                        temp_filled = fill_na_specific(df[selected_fill_columns_name], fill_specific_value)

                    if st.button("确认填充"):
                        df = temp_filled
                        st.write(df)

                elif process_way == '批量替换':
                    st.write(2)
                    replace_way = st.radio(label="选择批量替换的方式", options=('全部替换', '部分替换'))
                    if replace_way == '全部替换':
                        st.write(1)
                        selected_replace_columns_name = st.selectbox(label='选择替换的列',
                                                                     options=['All columns(except numeric column)']+df_columns_name)
                        '''
                        st.write(np.issubdtype(df['id'][0], np.number))
                        st.write(is_numeric_dtype(df['id'][0]))
                        st.write(df['id'].dtype)
                        '''
                        p1, p2 = st.columns([1, 1])
                        with p1:
                            if selected_replace_columns_name != 'All columns(except numeric column)' \
                                    and df[selected_replace_columns_name].dtype == 'int64':
                                before_replaced_value = st.number_input(label='替换前的值', value=0, key='replace_int')
                            elif selected_replace_columns_name != 'All columns(except numeric column)' \
                                    and df[selected_replace_columns_name].dtype == 'float64':
                                before_replaced_value = st.number_input(label='替换前的值', format='%f', key='replace_float')
                            else:
                                before_replaced_value = st.text_input(label='替换前的值')
                        with p2:
                            if selected_replace_columns_name != 'All columns(except numeric column)' \
                                    and df[selected_replace_columns_name].dtype == 'int64':
                                after_replaced_value = st.number_input(label='替换后的值', value=0, key='replaced_int')
                            elif selected_replace_columns_name != 'All columns(except numeric column)' \
                                    and df[selected_replace_columns_name].dtype == 'float64':
                                after_replaced_value = st.number_input(label='替换前的值', format='%f', key='replaced_float')
                            else:
                                after_replaced_value = st.text_input(label='替换后的值')

                        if selected_replace_columns_name == 'All columns(except numeric column)':
                            temp_replaced_df = replace_all_all_columns(df, before_replaced_value, after_replaced_value)
                        elif selected_replace_columns_name in df.columns.to_list():
                            temp_replaced_df = replace_all_single_columns(df, selected_replace_columns_name,
                                                                          before_replaced_value, after_replaced_value)

                    elif replace_way == '部分替换':
                        st.write(2)
                        # df_string_columns_name = [i for i in df.columns.to_list() if str(type(df[i][0])) == "<class 'str'>"]
                        df_string_columns_name = [i for i in df.columns.to_list() if df[i].dtype == 'object']

                        selected_part_replace_columns_name = st.selectbox(label='选择替换的列',
                                                                     options=df_string_columns_name)
                        p1, p2 = st.columns([1, 1])
                        with p1:
                            if df[selected_part_replace_columns_name].dtype == 'int64':
                                before_part_replaced_value = st.number_input(label='替换前的值', value=0, key='part_replace_int')
                            elif df[selected_part_replace_columns_name].dtype == 'float64':
                                before_part_replaced_value = st.number_input(label='替换前的值', format='%f', key='part_replace_float')
                            else:
                                before_part_replaced_value = st.text_input(label='替换前的值')
                        with p2:
                            if df[selected_part_replace_columns_name].dtype == 'int64':
                                after_part_replaced_value = st.number_input(label='替换后的值', value=0, key='part_replaced_int')
                            elif df[selected_part_replace_columns_name].dtype == 'float64':
                                after_part_replaced_value = st.number_input(label='替换前的值', format='%f', key='part_replaced_float')
                            else:
                                after_part_replaced_value = st.text_input(label='替换后的值')

                        temp_replaced_df = replace_part_single_columns(df, selected_part_replace_columns_name,
                                                                          before_part_replaced_value, after_part_replaced_value)


                    if st.button('确认替换'):
                        df = temp_replaced_df
                        st.write(df)

        # 功能4：增加用户新增的行或列
        with st.expander(label="功能4：增加用户新增的行或列", expanded=False):
            with st.container():
                df_columns_name = df.columns.to_list()
                add_list = [[] for _ in range(len(df.columns))]
                p1, p2 = st.columns([1, 3])
                with p1:
                    for i in range(len(df_columns_name)):
                        if df[df_columns_name[i]].dtype == 'int64':
                            add_list[i] = st.number_input(label=df_columns_name[i], value=0)
                        elif df[df_columns_name[i]].dtype == 'float64':
                            add_list[i] = st.number_input(label=df_columns_name[i], format='%f')
                        else:
                            add_list[i] = st.text_input(label=df_columns_name[i], placeholder=df_columns_name[i] + '=\n')
                    if st.button('确认增加'):
                        st.write('success')
                        add_temp_df = pd.DataFrame(data=np.array(add_list).reshape(1, len(df.columns)), columns=df_columns_name)
                        for i in range(len(df.columns)):
                            if df[df_columns_name[i]].dtype == 'int64':
                                add_temp_df[df_columns_name[i]] = add_temp_df[df_columns_name[i]].astype('int64')
                            elif df[df_columns_name[i]].dtype == 'float64':
                                add_temp_df[df_columns_name[i]] = add_temp_df[df_columns_name[i]].astype('float64')
                            elif df[df_columns_name[i]].dtype == 'bool':
                                add_temp_df[df_columns_name[i]] = add_temp_df[df_columns_name[i]].astype('bool')
                        df = df.append(add_temp_df, ignore_index=True)

                with p2:
                    st.write(1)
                    st.write(df)







        # 功能5：删除用户选定的行或列
        with st.expander(label="功能5：删除用户选定的行或列", expanded=False):
            with st.container():
                df_columns_name = df.columns.to_list()
                p1, p2 = st.columns([1, 1])
                with p1:
                    deleted_row_way = st.radio(label="选择你要删除的方式", options=('删除单行', '删除多行'))
                    if deleted_row_way == '删除单行':
                        selected_row_index = st.number_input(label='输入你要删除的行索引',
                                                             min_value=0,
                                                             max_value=df.shape[0] - 1,
                                                             format='%d')
                        # st.write('你要删除的行索引是：', selected_row_index)
                        temp_deleted_row = df.drop(labels=selected_row_index, axis=0, inplace=False)
                        st.write(temp_deleted_row)

                    elif deleted_row_way == '删除多行':
                        start_row, end_row = st.select_slider(
                            label='选择你要删除的行区间',
                            options=df.index.to_list(),
                            value=(0, int(df.shape[0] / 2)))
                        st.write('你选择的行区间为', start_row, 'and', end_row)
                        temp_deleted_row = df
                        for i in range(start_row, end_row + 1):
                            temp_deleted_row = temp_deleted_row.drop(labels=i, axis=0, inplace=False)
                        st.write(temp_deleted_row)

                    if st.button("确认删除行"):
                        df = temp_deleted_row
                        st.write(df)

                with p2:
                    selected_columns = st.multiselect(label="选择删除的列", options=df_columns_name)
                    temp_deleted_columns = df.drop(labels=selected_columns, axis=1, inplace=False)
                    st.write(temp_deleted_columns)
                    if st.button("确认删除列"):
                        df = temp_deleted_columns
                        st.write(df)

        # 功能6：修改列名或单元内容
        with st.expander(label="功能6：修改列名或单元内容", expanded=False):
            with st.container():
                st.write("功能6：修改列名或单元内容")
                df_columns_name = df.columns.to_list()
                modify_way = st.radio(label="选择你要修改的对象", options=('修改列名', '修改单元内容'))
                if modify_way == '修改列名':

                    selected_modify_col_name = st.selectbox(label='你想要修改哪个列名', options=df_columns_name)
                    modified_col_temp_name = st.text_input(label='请输入修改后的列名', value=selected_modify_col_name)
                    st.write('修改后的列名为：', modified_col_temp_name)
                    modified_temp_df = df.rename(columns={selected_modify_col_name: modified_col_temp_name})
                    st.write(modified_temp_df.head(5))

                    if st.button("确认修改"):
                        st.write('success')
                        df = modified_temp_df
                        st.write(df.head(5))

                elif modify_way == '修改单元内容':
                    st.write(2)
                    selected_modify_row_index = st.number_input(label='输入你要修改的行索引',
                                                                min_value=0,
                                                                max_value=df.shape[0] - 1,
                                                                format='%d')
                    selected_modify_col_name = st.selectbox(label='选择你要修改单元所在的列', options=df_columns_name)
                    st.write('你选择的行索引为：', selected_modify_row_index, '你选择的所在列为：', selected_modify_col_name)
                    st.write('该单元原本的内容为：', df.loc[selected_modify_row_index][selected_modify_col_name])
                    modified_cell_temp_value = st.text_input(label='请输入修改后的单元内容',
                                                             value=df.loc[selected_modify_row_index][selected_modify_col_name])
                    st.write('修改后的单元内容为：', modified_cell_temp_value)

                    modified_temp_df = df

                    if df[selected_modify_col_name].dtype != 'object':
                        if df.loc[selected_modify_row_index][selected_modify_col_name].dtype == 'int64':
                            modified_cell_temp_value = int(modified_cell_temp_value)
                        elif df.loc[selected_modify_row_index][selected_modify_col_name].dtype == 'float64':
                            modified_cell_temp_value = float(modified_cell_temp_value)
                        elif df.loc[selected_modify_row_index][selected_modify_col_name].dtype == 'bool':
                            modified_cell_temp_value = bool(0 if modified_cell_temp_value == 'False' or modified_cell_temp_value == 'false' else 1)

                    modified_temp_df.iloc[int(selected_modify_row_index), df_columns_name.index(
                        selected_modify_col_name)] = modified_cell_temp_value

                    if st.button("确认修改"):
                        st.write('success')
                        df = modified_temp_df
                        st.write(df)

        # 功能7：查找含有用户输入关键字的行或列
        with st.expander(label="功能7：查找含有用户输入关键字的行或列", expanded=False):
            with st.container():
                st.write("功能7：查找含有用户输入关键字的行或列")
                df_columns_name = df.columns.to_list()
                p1, p2 = st.columns([1, 1])
                with p1:
                    search_way = st.radio(label='选择查找的方式', options=('根据内容查找对应位置', '根据位置查找对应内容', '根据多列的内容查找对应位置'))
                    if search_way == '根据内容查找对应位置':
                        search_type = st.radio(label='选择查找的数据类型', options=('数值型', '字符串型'))
                        if search_type == '数值型':
                            search_location = st.number_input(label='输入你要查询的数值内容', value=0)
                            search_result = search_location_numeric(df, search_location)
                        elif search_type == '字符串型':
                            search_location = st.text_input(label='输入你要查询的字符串内容', value=0)
                            search_result = search_location_string(df, search_location)
                    elif search_way == '根据位置查找对应内容':
                        selected_search_column = st.selectbox(label='选择你要查看内容所在的列', options=df_columns_name)
                        selected_search_row = st.number_input(label='输入你要查看内容所在的行', value=0, max_value=df.shape[0]-1)
                        search_result = search_value_numeric(df, selected_search_column, selected_search_row)
                    elif search_way == '根据多列的内容查找对应位置':
                        selected_search_columns = st.multiselect(label="选择你要查找内容对应的列", options=df_columns_name)
                        value_columns = [1 for _ in range(len(selected_search_columns))]
                        for i in range(len(selected_search_columns)):
                            if df[selected_search_columns[i]].dtype == 'int64':
                                value_columns[i] = st.number_input(label='请输入【'+selected_search_columns[i]+'】列中的值', value=1)
                                value_columns[i] = int(value_columns[i])
                            elif df[selected_search_columns[i]].dtype == 'float64':
                                value_columns[i] = st.number_input(label='请输入【' + selected_search_columns[i] + '】列中的值', format='%f')
                                value_columns[i] = float(value_columns[i])
                            else:
                                value_columns[i] = st.text_input(label='请输入【'+selected_search_columns[i]+'】列中的值')

                        search_result = search_location_by_columns(df, selected_search_columns, value_columns)

                with p2:
                    if st.button('开始查找'):

                        if search_way == '根据内容查找对应位置':
                            for i in range(0, search_result[2]):
                                st.write('第', i + 1, '次 列：[', search_result[0][i], ']  行：', search_result[1][i])
                            if search_result[2] == 0:
                                st.write('抱歉，查找不到。')
                            st.write('总共出现次数：', search_result[2])
                        elif search_way == '根据位置查找对应内容':
                            st.write('列[', selected_search_column, ']，行 ', selected_search_row, '的内容为：', search_result)
                        elif search_way == '根据多列的内容查找对应位置':
                            st.write(value_columns)
                            st.write(search_result)
                            for i in range(len(search_result)):
                                st.write('行索引号为', search_result[i], ' 符合查找要求， 其行内容为：')
                                # st.text(df.loc[search_result[i], df_columns_name])
                                # st.dataframe(df[search_result[i]:search_result[i]+1])
                                st.write(df[search_result[i]:search_result[i]+1])

        # 功能8：新数据导出
        with st.expander(label="功能8：新数据导出", expanded=False):
            with st.container():
                p1, p2 = st.columns([1, 1])
                with p1:
                    if data is not None:
                        st.download_button(label="Download data as CSV",
                                           data=convert2csv_df(df),
                                           file_name='test.csv',
                                           mime='text/csv',
                                           help='click to download the above data as CSV'
                                           )
                with p2:
                    if data is not None:
                        st.download_button(label="Download data as XLSX",
                                           data=convert2excel_df(df),
                                           file_name='test.xlsx',
                                           mime='text/xlsx',
                                           help='click to download the above data as XLSX(one sheet)'
                                           # https://discuss.streamlit.io/t/download-xlsx-file-with-multiple-sheets-in-streamlit/11509/2
                                           )

            '''
            st.button(label='Download data as XLSX',
                      on_click=convert2xlsx_df(df),
                      help='click to download the above data as XLSX')
            '''

        # 功能9：展示各个维度的参数
        with st.expander(label="功能9：展示各个维度的参数", expanded=False):
            if st.checkbox("Show Shape"):
                st.write(df.shape)
            if st.checkbox("Show Columns"):
                # df_columns_name = df.columns.to_list()
                st.write(df_columns_name)
            if st.checkbox("Select Columns To Show"):
                selected_columns = st.multiselect("Selected Columns", df_columns_name)
                new_df = df[selected_columns]
                if not new_df.empty:
                    st.dataframe(new_df)
            if st.checkbox("Show Summary"):
                st.write(df.describe())


# 数据分析
def page2():
    st.write("This is page2")
    # st.dataframe(df)
    data = st.file_uploader("上传数据", type=["csv", 'txt', 'xlsx', 'xls'])
    st.write("功能1：自动根据数据产生几张简单图表（container）")
    st.write("功能2：用户选择数据交互产生图表（container）")
    st.write("功能3：生成词云（不同列、行或全局）")
    st.write("功能4：")


# 数据挖掘
def page3():
    st.write("This is page3")
    st.write("KNN(container)")
    st.write("K-mean(container)")
    st.write("决策树(container)")
    st.write("线性回归(container)")


# 性别分类
def page4():
    st.write("This is page4")


# 密码强度检测
def page5():
    st.write("This is page5")


# 汽车评价
def page6():
    st.write("This is page6")


# 人脸检测
def page7():
    st.write("This is page7")


# 概要和实体检查器
def page8():
    st.write("This is page8")


# NLPiffy
def page9():
    st.write("This is page9")


# 文档编辑
def page10():
    st.write("This is page10")


# 案例展示
def pageExample():
    st.write("This is page of example")


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
    if df[df_columns_name[i]].dtype == 'string':
        index = 0
    elif df[df_columns_name[i]].dtype == 'int64':
        index = 1
    elif df[df_columns_name[i]].dtype == 'float64':
        index = 2
    elif df[df_columns_name[i]].dtype == 'bool':
        index = 3
    return index


def drop_na_any(df):
    st.write('success')
    df = df.dropna(axis=0, how='any', subset=list(df.keys()))
    return df


def drop_na_all(df):
    st.write('success')
    df = df.dropna(axis=0, how='all', subset=list(df.keys()))
    return df


def drop_duplicates_first(df):
    st.write('success')
    df = df.drop_duplicates(subset=list(df.keys()), keep='first')
    return df


def drop_duplicates_last(df):
    st.write('success')
    df = df.drop_duplicates(subset=list(df.keys()), keep='last')
    return df


def fill_na_bfill(df):
    st.write('success')
    df = df.fillna(method='bfill')
    return df


def fill_na_ffill(df):
    st.write('success')
    df = df.fillna(method='ffill')
    return df


def fill_na_specific(df, fill_specific_value):
    st.write('success')
    df = df.fillna(value=fill_specific_value)
    return df


def replace_all_all_columns(df, to_replace, value):
    st.write('success')
    df = df.replace(to_replace, value, inplace=False)
    return df


def replace_all_single_columns(df, col, to_replace, value):
    st.write('success')
    df[col] = df[col].replace(to_replace, value, inplace=False)
    return df


def replace_part_all_columns(df, to_replace, value):
    st.write('success')
    df = df.str.replace(to_replace, value)
    return df


def replace_part_single_columns(df, col, to_replace, value):
    st.write('success')
    df[col] = df[col].str.replace(to_replace, value)
    return df


def search_location_numeric(df, value):
    st.write('success')
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
    st.write('success')
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
    st.write('success')
    value = df[col][row]
    return value


def search_value_string(df, col, row):
    st.write('success')
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

