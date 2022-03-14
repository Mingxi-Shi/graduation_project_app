
from functions.page2_func import *


def page2():
    sample_or_upload = st.sidebar.radio("上传数据集或使用内置数据集", options=['上传数据集', '内置数据集'])
    if sample_or_upload == "上传数据集":
        data = st.sidebar.file_uploader("上传数据", type=["csv", 'txt', 'xlsx', 'xls'], key='page2_file_upload')
        if data is not None:
            if data.name[-3:] == "csv" or data.name[-3:] == "txt":
                df = pd.read_csv(data)
            elif data.name[-3:] == "xls" or data.name[-4:] == "xlsx":
                df = pd.read_excel(data)
    elif sample_or_upload == "内置数据集":
        inner_datasets = []
        for dataset in os.listdir('datasets'):  # 用os库获取文件夹下所有文件名
            inner_datasets.append(dataset)
        data = st.sidebar.selectbox(label="选择数据集", options=inner_datasets)
        if data[-3:] == "csv" or data[-3:] == "txt":
            df = pd.read_csv('datasets/'+data)
        elif data[-3:] == "xls" or data[-4:] == "xlsx":
            df = pd.read_excel('datasets/'+data)
    if data is not None:

        selected_menu = st.sidebar.selectbox(label="选择功能", options=["数据profiler", "生成图表"])
        if selected_menu == "数据profiler":
            navigation_bar = option_menu(menu_title=None, options=["数据报告", "数据关系图"],
                                         icons=["hypnotize", "hypnotize"], menu_icon="list-task",
                                         default_index=0, orientation="horizontal")
            if navigation_bar == "数据报告":
                if st.button("开始生成数据报告"):
                    # pr = ProfileReport(df=df, explorative=True, orange_mode=True)
                    pr = ProfileReport(df=df)
                    st_profile_report(pr)
            elif navigation_bar == "数据关系图":
                generate_correlated_chart(df)
        elif selected_menu == "生成图表":
            # 配置 ag-grid
            gb = GridOptionsBuilder.from_dataframe(df)

            update_mode = st.sidebar.selectbox("Update Mode", ["SELECTION_CHANGED", "FILTERING_CHANGED"], index=1)
            update_mode_value = GridUpdateMode.__members__[update_mode]

            gb.configure_default_column(aggFunc='sum', resizable=True, sorteable=True, filterable=True, groupable=True,
                                        editable=True, enablePivot=True)  # 配置单元格内容可修改
            gb.configure_side_bar(filters_panel=True, columns_panel=True)  # 侧边栏

            gb.configure_selection("multiple")
            gb.configure_columns(column_names=str(df.columns.to_list()), enablePivot=True)
            with st.form("edit_form"):
                ag = AgGrid(
                    dataframe=df,
                    gridOptions=gb.build(),
                    height=494,
                    fit_columns_on_grid_load=False,
                    reload_data=False,
                    enable_enterprise_modules=True,
                    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
                    update_mode=update_mode_value,
                )

                submitted = st.form_submit_button(label="完成")
                if submitted:
                    if len(ag['data']) == 1 or len(ag["selected_rows"]) == 1:
                        st.info("筛选或选择的行数需大于或等于2, 请重新提交")
                    else:
                        st.success("提交成功")

            if update_mode == "SELECTION_CHANGED":
                if ag["selected_rows"]:
                    df = pd.DataFrame(ag["selected_rows"])
            elif update_mode == "FILTERING_CHANGED":
                df = ag['data']
            # 选择列和行
            df_columns_name = df.columns.to_list()
            p1, p2 = st.columns([1, 1])
            with p1:
                selected_columns = st.multiselect(label="选择需要的列(可多选)", options=df_columns_name, default=df_columns_name)

            with p2:
                selected_start_row, selected_end_row = st.select_slider(
                    label='选择需要的行区间',
                    options=df.index.to_list(),
                    value=(0, int(df.shape[0])-1))
                st.write('你选择的行区间为', selected_start_row, 'and', selected_end_row)
                result = dataset_information(df)
                st.write("行数：", result[0][0], "列数：", result[0][1])
                st.write("该表格的字符串列有：" + str(result[1]["string"]))
                st.write("该表格的整数型列有：" + str(result[1]["int"]))
                st.write("该表格的浮点型列有：" + str(result[1]["float"]))
                st.write("该表格的布尔型列有：" + str(result[1]["bool"]))

            if len(selected_columns) != 0 and selected_end_row:
                df = df.loc[selected_start_row:selected_end_row]
                df = df[selected_columns]
                p1.write(df)

            # st.dataframe(df, height=500)
            col1, col2 = st.columns([1, 1])
            with col1:
                selected_chart_type = st.selectbox(label="选择图表类型", options=["直方图", "折线图", "散点图"])
            with col2:
                st.write(1)

            generate_chart(df, chart_type=selected_chart_type)


