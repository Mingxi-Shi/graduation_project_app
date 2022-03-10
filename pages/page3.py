import ast

import pandas as pd
import streamlit
import streamlit.config_option

from functions.page3_func import *


def page3():

    # # 这个可以对原有的列进行计算，生成新的列
    # # gb.configure_column('virtual column a + b', valueGetter='Number(data.a) + Number(data.b)',
    # #                     cellRenderer='agAnimateShowChangeCellRenderer', editable='false', type=['numericColumn'])

    data = st.file_uploader("上传数据", type=["csv", 'txt', 'xlsx', 'xls'], key='pagetest_file_upload')
    if data is not None:
        if data.name[-3:] == "csv" or data.name[-3:] == "txt":
            df = pd.read_csv(data)
        elif data.name[-3:] == "xls" or data.name[-4:] == "xlsx":
            df = pd.read_excel(data)

        gb = GridOptionsBuilder.from_dataframe(df)

        return_mode = st.sidebar.selectbox("Return Mode", list(DataReturnMode.__members__), index=1)
        return_mode_value = DataReturnMode.__members__[return_mode]

        update_mode = st.sidebar.selectbox("Update Mode", list(GridUpdateMode.__members__), index=6)
        update_mode_value = GridUpdateMode.__members__[update_mode]

        col1, col2, col3 = st.sidebar.columns([3, 2, 2])
        with col1:
            selected_theme = st.selectbox("表格主题", ["streamlit", "light", "dark", "blue", "fresh", "material"])  # 选择编辑表单主题
        with col2:
            selection_mode = st.radio("选择模式", ['单行', '多行'])
        with col3:
            click_or_ctrl = st.radio("选择方式", ["鼠标", "Ctrl键"])

        if selection_mode == "单行":
            gb.configure_selection("single", use_checkbox=False, rowMultiSelectWithClick=True if click_or_ctrl == "鼠标" else False,
                                   suppressRowDeselection=True if click_or_ctrl == "Ctrl键" else False)
        elif selection_mode == "多行":
            gb.configure_selection("multiple", use_checkbox=False, rowMultiSelectWithClick=True if click_or_ctrl == "鼠标" else False,
                                   suppressRowDeselection=True if click_or_ctrl == "Ctrl键" else False)

        col4, col5 = st.sidebar.columns([1, 1])
        with col4:
            is_pagination = st.checkbox(label="是否分页", value=False)
        with col5:
            pagination_PageSize = 10
            if is_pagination:
                pagination_PageSize = st.number_input(label="分页大小", min_value=1, value=10)

        gb.configure_default_column(aggFunc='sum', resizable=True, sorteable=True, filterable=True, groupable=True, editable=True, enablePivot=True)  # 配置单元格内容可修改
        gb.configure_side_bar(filters_panel=True, columns_panel=True)  # 侧边栏
        gb.configure_pagination(enabled=is_pagination, paginationAutoPageSize=False, paginationPageSize=pagination_PageSize)  # 分页
        gb.configure_selection("multiple")
        gb.configure_columns(column_names=str(df.columns.to_list()), enablePivot=True)
        with st.form("edit_form"):
            ag = AgGrid(
                dataframe=df,
                gridOptions=gb.build(),
                height=494,
                fit_columns_on_grid_load=False,
                reload_data=False,
                theme=selected_theme,
                enable_enterprise_modules=True,
                data_return_mode=return_mode_value,
                update_mode=update_mode_value,
            )
            submitted = st.form_submit_button(label="完成")
            if submitted:
                st.write(1)
                df = ag['data']
        st.dataframe(df, height=500)
        st.write(ag)

        test = ag["selected_rows"]
        test_df = pd.DataFrame(test, columns=df.columns[1:])
        # st.bar_chart(test_df)

        if data is not None:
            p1, p2 = st.columns([1, 6])
            with p1:
                st.download_button(label="Download data as CSV",
                                   data=convert2csv_df(df),
                                   file_name='test.csv',
                                   mime='text/csv',
                                   key='download_as_csv',
                                   help='click to download the above data as CSV'
                                   )
            with p2:
                st.download_button(label="Download data as XLSX",
                                   data=convert2excel_df(df),
                                   file_name='test.xlsx',
                                   mime='text/xlsx',
                                   key='download_as_xlsx',
                                   help='click to download the above data as XLSX(one sheet)'
                                   )


