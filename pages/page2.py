
from functions.page2_func import *


# 数据分析
def page2():
    st.write("This is page2")
    data = st.file_uploader("上传数据", type=["csv", 'txt', 'xlsx', 'xls'], key='page2_file_upload')
    if data is not None:
        if data.name[-3:] == "csv" or data.name[-3:] == "txt":
            df = pd.read_csv(data)
            st.dataframe(df.head(20))
        elif data.name[-3:] == "xls" or data.name[-4:] == "xlsx":
            df = pd.read_excel(data)
            st.dataframe(df.head(20))

        with st.expander(label="功能0：载入表格的基本信息", expanded=False):
            # 筛选不同数据类型的列（后期改为调用方法
            df_columns_name = df.columns.to_list()
            type_of_string_columns_name = []
            type_of_int_columns_name = []
            type_of_float_columns_name = []
            type_of_bool_columns_name = []
            type_of_date_columns_name = []

            for i in range(len(df.columns)):
                if df[df_columns_name[i]].dtype == 'object' and is_date(df[df_columns_name[i]][0]) is False:
                    type_of_string_columns_name.append(df_columns_name[i])
                elif df[df_columns_name[i]].dtype == 'int64':
                    type_of_int_columns_name.append(df_columns_name[i])
                elif df[df_columns_name[i]].dtype == 'float64':
                    type_of_float_columns_name.append(df_columns_name[i])
                elif df[df_columns_name[i]].dtype == 'bool':
                    type_of_bool_columns_name.append(df_columns_name[i])
                elif df[df_columns_name[i]].dtype == 'object' and is_date(df[df_columns_name[i]][0]) is True:
                    type_of_date_columns_name.append(df_columns_name[i])


            st.text("该表格的行数和列数：" + str(df.shape))
            st.text("该表格的数据按列的统计信息：" + "\n" + str(df.describe()))
            st.text("该表格的字符串列有：" + str(type_of_string_columns_name) + "\n" +
                    "该表格的整数型列有：" + str(type_of_int_columns_name) + "\n" +
                    "该表格的浮点型列有：" + str(type_of_float_columns_name) + "\n" +
                    "该表格的布尔型列有：" + str(type_of_bool_columns_name) + "\n" +
                    "该表格的日期型列有：" + str(type_of_date_columns_name) + "\n")

        with st.expander(label="功能1：自动根据数据产生几张简单图表（container）", expanded=False):

            # 方法一：直接random.choice随机选取一个
            # st.write("随机选取一列：", random.choice(type_of_float_columns_name))
            # 方法二：先random.shuffle，再输出第一个
            # random.shuffle(df_columns_name)
            # st.write(df_columns_name[0])

            if st.checkbox("生成数值型的图表"):
                if st.button("开始随机生成"):
                    random_number = random.randint(1, 9)
                    # st.write(random_number)
                    if random_number < 4:
                        # st.line_chart(data=df[type_of_float_columns_name], use_container_width=True)
                        # st.line_chart(data=df[type_of_int_columns_name], use_container_width=True)
                        st.line_chart(data=df[type_of_float_columns_name+type_of_int_columns_name], use_container_width=True)
                    elif (random_number >= 4) & (random_number < 7):
                        # st.area_chart(data=df[type_of_float_columns_name], use_container_width=True)
                        # st.area_chart(data=df[type_of_int_columns_name], use_container_width=True)
                        st.area_chart(data=df[type_of_float_columns_name+type_of_int_columns_name], use_container_width=True)
                    elif (random_number >= 7) & (random_number < 10):
                        # st.bar_chart(data=df[type_of_float_columns_name], use_container_width=True)
                        # st.bar_chart(data=df[type_of_int_columns_name], use_container_width=True)
                        st.bar_chart(data=df[type_of_float_columns_name+type_of_int_columns_name], use_container_width=True)

            if st.checkbox("生成字符串型的图表"):
                st.write(2222222222)
            if st.checkbox("生成布尔型的图表"):
                st.write(3333333333)
            # 根据数据类型，每一次按钮，根据随机数，随机生成一种图（不同类型的图，不同的列）

        with st.expander(label="功能2：用户选择数据交互产生图表（container）", expanded=False):
            st.write("---判断所选列的数据类型，限制可选择的图表类型")
            selected_column_names = st.multiselect(label='选择列(可多选)', options=df_columns_name)
            # -------------------------加限制语句----------------------------
            # -------------------------------------------------------------
            selected_type_of_plot = st.selectbox("选择图表类型", ["area", "bar", "line", "hist", "box", "kde"])
            if st.button("开始生成"):
                st.success("客制化列{}的{}图表生成中...".format(selected_column_names, selected_type_of_plot))

                if selected_type_of_plot == 'area':
                    selected_data = df[selected_column_names]
                    st.area_chart(selected_data)
                elif selected_type_of_plot == 'bar':
                    selected_data = df[selected_column_names]
                    st.bar_chart(selected_data)
                elif selected_type_of_plot == 'line':
                    selected_data = df[selected_column_names]
                    st.line_chart(selected_data)
                elif selected_type_of_plot == 'hist':
                    fig, ax = plt.subplots()
                    ax.hist(x=df[selected_column_names], bins=5)
                    st.pyplot(fig)
                elif selected_type_of_plot == 'box':
                    # fig, ax = plt.subplots()
                    # custom_plot = df[selected_column_names].plot(kind='box')
                    # st.write(custom_plot)
                    # st.pyplot(fig=plt)
                    # fig, ax = plt.subplots()
                    # ax.boxplot(x=df[selected_column_names])
                    # st.pyplot(fig)
                    # fig, ax = plt.subplots()
                    # df[selected_column_names].boxplot(column=selected_column_names, grid=False)
                    # st.pyplot(fig)
                    fig, ax = plt.subplots()
                    df[selected_column_names].plot.box()
                    st.pyplot(fig=plt)

                elif selected_type_of_plot == 'kde':
                    # fig, ax = plt.subplots()
                    # custom_plot = df[selected_column_names].plot(kind='kde')
                    # #st.write(custom_plot)
                    # st.pyplot(fig=plt)
                    fig, ax = plt.subplots()
                    df[selected_column_names].plot.kde()
                    st.pyplot(fig=plt)

            # -------

        with st.expander(label="功能3：生成词云", expanded=False):
            if type_of_string_columns_name:
                selected_column = st.selectbox(label="选择列生成词云图", options=type_of_string_columns_name)
                column_data_for_wc = df[selected_column]

                if st.button("开始生成", key='page2_generate_wc'):
                    txt = []
                    for i in column_data_for_wc:
                        txt.append(i)
                    txt = ",".join(str(i) for i in txt)

                    wc = WordCloud(font_path='fonts/宋体.ttc', background_color="white", collocations=False).generate(txt)

                    fig, ax = plt.subplots()
                    plt.imshow(wc)  # 以图片的形式显示词云
                    plt.axis("off")  # 关闭图像坐标系
                    st.pyplot(fig)  # 显示图片
                    # -------
            else:
                st.info("该表没有字符串类型数据可供生成词云图")