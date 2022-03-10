
from functions.page1_func import *


def page1():
    data = st.sidebar.file_uploader("上传数据", type=["csv", 'txt', 'xlsx', 'xls'], key='page1_file_upload')
    if data is not None:
        if data.name[-3:] == "csv" or data.name[-3:] == "txt":
            df = pd.read_csv(data)
            st.dataframe(df)
        elif data.name[-3:] == "xls" or data.name[-4:] == "xlsx":
            df = pd.read_excel(data)
            st.dataframe(df)

        # 功能0：修改列数据类型
        with st.expander(label="功能0：修改数据类型", expanded=False):
            df_columns_name = df.columns.to_list()
            modified_datatype = [' ' for _ in range(len(df.columns))]
            p1, p2 = st.columns([1, 5])
            with p1:
                for i in range(len(df_columns_name)):
                    modified_datatype[i] = st.selectbox(label='选择列 [ ' + df_columns_name[i] + ' ]的数据类型',
                                                        options=['string', 'int64', 'float64', 'bool'], key=i,
                                                        index=judge_original_datatype(df, i))
            with p2:
                st.text('')
                st.text('')
            if st.button("确认修改", key='modify_datatype'):
                df = convert_df_columns_datatype(df, df_columns_name, modified_datatype)
                p2.dataframe(df)

        # 功能1：数据去空（不同条件）
        with st.expander(label="功能1：去除空行（不同条件）", expanded=False):
            st.write("存在空值的行数据：\n", df.loc[df.isnull().any(axis=1)])
            # st.write("存在空值的行数据：\n", df.loc[df.notnull().all(axis=1)])
            drop_na_row = st.radio(label="选择你要去空的方式", options=('by row & any', 'by row & all'))
            # st.dataframe(df)
            if st.button("确认去空"):
                if drop_na_row == 'by row & any':
                    df = drop_na_any(df)
                elif drop_na_row == 'by row & all':
                    df = drop_na_all(df)
                st.dataframe(df)

        # 功能2：数据去重（不同条件）
        with st.expander(label="功能2：去除重复行（不同条件）", expanded=False):
            drop_duplicates = st.radio(label="选择你要去重的方式", options=('first', 'last'))
            # st.dataframe(df)
            if st.button("确认去重"):
                if drop_duplicates == 'first':
                    df = drop_duplicates_first(df)
                elif drop_duplicates == 'last':
                    df = drop_duplicates_last(df)
                st.dataframe(df)

        # 功能3：空值填充和批量替换
        with st.expander(label="功能3：空值填充和批量替换", expanded=False):
            process_way = st.radio(label="选择你进行的操作", options=('空值填充', '批量替换'))
            df_columns_name = df.columns.to_list()
            if process_way == '空值填充':
                fill_na_way = st.radio(label="选择填充空值的方式", options=('向前填充(bfill)', '向后填充(ffill)', '填充指定的值'))
                if fill_na_way == '向前填充(bfill)' or fill_na_way == '向后填充(ffill)':
                    selected_fill_columns_name = st.multiselect(label='选择你要空值填充的列（可多选）', options=df_columns_name)
                else:
                    selected_fill_columns_name = st.selectbox(label='选择你要空值填充的列', options=df_columns_name)
                    if df[selected_fill_columns_name].dtype == 'int64':
                        fill_specific_value = st.number_input(label='输入你要填充的值', value=0, key='fill_int')
                    elif df[selected_fill_columns_name].dtype == 'float64':
                        fill_specific_value = st.number_input(label='输入你要填充的值', format='%f', key='fill_float')
                    else:
                        fill_specific_value = st.text_input(label='输入你要填充的值', key='fill_str')

                if st.button("确认填充"):
                    if fill_na_way == '向前填充(bfill)':
                        df = fill_na_bfill(df, selected_fill_columns_name)
                    elif fill_na_way == '向后填充(ffill)':
                        df = fill_na_ffill(df, selected_fill_columns_name)
                    else:
                        df = fill_na_specific(df, selected_fill_columns_name, fill_specific_value)
                    st.dataframe(df)

            elif process_way == '批量替换':
                replace_way = st.radio(label="选择批量替换的方式", options=('全部替换', '部分替换'))
                if replace_way == '全部替换':
                    selected_replace_columns_name = st.selectbox(label='选择替换的列',
                                                                 options=['All columns(except numeric column)'] + df_columns_name)
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

                elif replace_way == '部分替换':

                    # df_string_columns_name = [i for i in df.columns.to_list() if str(type(df[i][0])) == "<class 'str'>"]
                    df_string_columns_name = [i for i in df.columns.to_list() if df[i].dtype == 'object']

                    selected_part_replace_columns_name = st.selectbox(label='选择替换的列',
                                                                      options=df_string_columns_name)
                    p1, p2 = st.columns([1, 1])
                    with p1:
                        if df[selected_part_replace_columns_name].dtype == 'int64':
                            before_part_replaced_value = st.number_input(label='替换前的值', value=0,
                                                                         key='part_replace_int')
                        elif df[selected_part_replace_columns_name].dtype == 'float64':
                            before_part_replaced_value = st.number_input(label='替换前的值', format='%f',
                                                                         key='part_replace_float')
                        else:
                            before_part_replaced_value = st.text_input(label='替换前的值')
                    with p2:
                        if df[selected_part_replace_columns_name].dtype == 'int64':
                            after_part_replaced_value = st.number_input(label='替换后的值', value=0,
                                                                        key='part_replaced_int')
                        elif df[selected_part_replace_columns_name].dtype == 'float64':
                            after_part_replaced_value = st.number_input(label='替换前的值', format='%f',
                                                                            key='part_replaced_float')
                        else:
                            after_part_replaced_value = st.text_input(label='替换后的值')

                if st.button('确认替换'):
                    if replace_way == "全部替换":
                        if selected_replace_columns_name == 'All columns(except numeric column)':
                            df = replace_all_all_columns(df, before_replaced_value, after_replaced_value)
                        elif selected_replace_columns_name in df.columns.to_list():
                            df = replace_all_single_columns(df, selected_replace_columns_name, before_replaced_value,
                                                            after_replaced_value)
                    elif replace_way == "部分替换":
                        df = replace_part_single_columns(df, selected_part_replace_columns_name, before_part_replaced_value,
                                                         after_part_replaced_value)
                    st.dataframe(df)

        # 功能4：增加用户新增的行或列
        with st.expander(label="功能4：增加用户新增的行", expanded=False):
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
                        add_list[i] = st.text_input(label=df_columns_name[i],
                                                    placeholder=df_columns_name[i] + '=\n')
                if st.button('确认增加'):
                    st.write('success')
                    add_temp_df = pd.DataFrame(data=np.array(add_list).reshape(1, len(df.columns)),
                                               columns=df_columns_name)
                    for i in range(len(df.columns)):
                        if df[df_columns_name[i]].dtype == 'int64':
                            add_temp_df[df_columns_name[i]] = add_temp_df[df_columns_name[i]].astype('int64')
                        elif df[df_columns_name[i]].dtype == 'float64':
                            add_temp_df[df_columns_name[i]] = add_temp_df[df_columns_name[i]].astype('float64')
                        elif df[df_columns_name[i]].dtype == 'bool':
                            add_temp_df[df_columns_name[i]] = add_temp_df[df_columns_name[i]].astype('bool')
                    df = df.append(add_temp_df, ignore_index=True)

            with p2:
                st.write(df)

        # 功能5：删除用户选定的行或列
        with st.expander(label="功能5：删除用户选定的行或列", expanded=False):
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
                elif deleted_row_way == '删除多行':
                    start_row, end_row = st.select_slider(
                        label='选择你要删除的行区间',
                        options=df.index.to_list(),
                        value=(0, int(df.shape[0] / 2)))
                    st.write('你选择的行区间为', start_row, 'and', end_row)

                if st.button("确认删除行"):
                    if deleted_row_way == '删除单行':
                        df = df.drop(labels=selected_row_index, axis=0, inplace=False)
                    elif deleted_row_way == '删除多行':
                        for i in range(start_row, end_row + 1):
                            df = df.drop(labels=i, axis=0, inplace=False)
                    st.dataframe(df)

            with p2:
                selected_columns = st.multiselect(label="选择删除的列", options=df_columns_name)
                if st.button("确认删除列"):
                    df = df.drop(labels=selected_columns, axis=1, inplace=False)
                    st.dataframe(df)

        # 功能6：修改列名或单元内容
        with st.expander(label="功能6：修改列名或单元内容", expanded=False):

            st.write("功能6：修改列名或单元内容")
            df_columns_name = df.columns.to_list()
            modify_way = st.radio(label="选择你要修改的对象", options=('修改列名', '修改单元内容'))
            if modify_way == '修改列名':
                selected_modify_col_name = st.selectbox(label='你想要修改哪个列名', options=df_columns_name)
                modified_col_temp_name = st.text_input(label='请输入修改后的列名', value=selected_modify_col_name)
                st.write('修改后的列名为：', modified_col_temp_name)

                if st.button("确认修改"):
                    df = df.rename(columns={selected_modify_col_name: modified_col_temp_name})
                    st.dataframe(df)

            elif modify_way == '修改单元内容':
                selected_modify_row_index = st.number_input(label='输入你要修改的行索引',
                                                            min_value=0,
                                                            max_value=df.shape[0] - 1,
                                                            format='%d')
                selected_modify_col_name = st.selectbox(label='选择你要修改单元所在的列', options=df_columns_name)
                st.write('你选择的行索引为：', selected_modify_row_index, '你选择的所在列为：', selected_modify_col_name)
                st.write('该单元原本的内容为：', df.loc[selected_modify_row_index][selected_modify_col_name])
                modified_cell_temp_value = st.text_input(label='请输入修改后的单元内容',
                                                         value=df.loc[selected_modify_row_index][
                                                             selected_modify_col_name])
                st.write('修改后的单元内容为：', modified_cell_temp_value)

                if st.button("确认修改"):
                    if df[selected_modify_col_name].dtype != 'object':
                        if df.loc[selected_modify_row_index][selected_modify_col_name].dtype == 'int64':
                            modified_cell_temp_value = int(modified_cell_temp_value)
                        elif df.loc[selected_modify_row_index][selected_modify_col_name].dtype == 'float64':
                            modified_cell_temp_value = float(modified_cell_temp_value)
                        elif df.loc[selected_modify_row_index][selected_modify_col_name].dtype == 'bool':
                            modified_cell_temp_value = bool(
                                0 if modified_cell_temp_value == 'False' or modified_cell_temp_value == 'false' else 1)
                    df[selected_modify_col_name][selected_modify_row_index] = modified_cell_temp_value
                    st.dataframe(df)

        # 功能7：查找含有用户输入关键字的行或列
        with st.expander(label="功能7：查找含有用户输入关键字的行或列", expanded=False):
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
                    selected_search_row = st.number_input(label='输入你要查看内容所在的行', value=0, max_value=df.shape[0] - 1)
                    search_result = search_value_numeric(df, selected_search_column, selected_search_row)
                elif search_way == '根据多列的内容查找对应位置':
                    selected_search_columns = st.multiselect(label="选择你要查找内容对应的列", options=df_columns_name)
                    value_columns = [1 for _ in range(len(selected_search_columns))]
                    for i in range(len(selected_search_columns)):
                        if df[selected_search_columns[i]].dtype == 'int64':
                            value_columns[i] = st.number_input(label='请输入【' + selected_search_columns[i] + '】列中的值',
                                                               value=1)
                            value_columns[i] = int(value_columns[i])
                        elif df[selected_search_columns[i]].dtype == 'float64':
                            value_columns[i] = st.number_input(label='请输入【' + selected_search_columns[i] + '】列中的值',
                                                               format='%f')
                            value_columns[i] = float(value_columns[i])
                        else:
                            value_columns[i] = st.text_input(label='请输入【' + selected_search_columns[i] + '】列中的值')

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
                            st.write(df[search_result[i]:search_result[i] + 1])

        # 功能8：新数据导出
        with st.expander(label="功能8：数据导出", expanded=False):
            if data is not None:
                st.download_button(label="Download data as CSV",
                                   data=convert2csv_df(df),
                                   file_name='test.csv',
                                   mime='text/csv',
                                   key='download_as_csv',
                                   help='click to download the above data as CSV'
                                   )

                st.download_button(label="Download data as XLSX",
                                   data=convert2excel_df(df),
                                   file_name='test.xlsx',
                                   mime='text/xlsx',
                                   key='download_as_xlsx',
                                   help='click to download the above data as XLSX(one sheet)'
                                   # https://discuss.streamlit.io/t/download-xlsx-file-with-multiple-sheets-in-streamlit/11509/2
                                   )

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
