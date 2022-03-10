
from functions.page6_func import *


# 假数据生成
def page6():
    st.title("假数据生成器")

    menu = st.sidebar.selectbox("菜单", ["Home", "Customize"])
    if menu == "Home":
        st.subheader("主页")

        menu_1 = st.sidebar.selectbox(label="类型", options=["表格", "文本"])
        locale = st.sidebar.multiselect("选择语言环境", options=["en_US", "zh_CN"], default="zh_CN")

        if menu_1 == "表格":
            row_number = st.sidebar.number_input("数据行数", min_value=10, max_value=5000, value=10, step=1, format="%d")
            df = generate_profile(row_number, locale)
            st.dataframe(df)
            download_df(df)
        elif menu_1 == "文本":
            with st.expander(label="段落", expanded=False):
                if st.button("确认生成段落"):
                    result = generate_customized_text(locale, "paragraphs", 5, 0)
                    st.write(result)
            with st.expander(label="句子", expanded=False):
                if st.button("确认生成句子"):
                    result = generate_customized_text(locale, "sentences", 5, 0)
                    st.write(result)
            with st.expander(label="文本字符串", expanded=False):
                if st.button("确认生成文本字符串"):
                    result = generate_customized_text(locale, "texts", 5, 160)
                    st.write(result)
            with st.expander(label="词组", expanded=False):
                if st.button("确认生成词组"):
                    result = generate_customized_text(locale, "words", 5, 0)
                    st.write(result)
    elif menu == "Customize":
        st.subheader("客制化假数据")
        menu_2 = st.sidebar.selectbox(label="类型", options=["表格", "文本"])
        locale = st.sidebar.multiselect("选择语言环境", options=["en_US", "zh_CN"], default="zh_CN")

        if menu_2 == "表格":
            row_number = st.sidebar.number_input("数据行数", 10, 10000)
            profile_options_list = ['username', 'name', 'sex', 'address', 'mail', 'birthdate', 'job', 'company', 'ssn',
                                    'residence', 'current_location', 'blood_group', 'website']
            profile_fields = st.sidebar.multiselect(label="可选字段", options=profile_options_list, default=['username', 'name'])

            df = generate_customized_profile(row_number, locale, profile_fields)
            st.dataframe(df)
            download_df(df)
        elif menu_2 == "文本":
            with st.expander(label="客制化生成段落", expanded=False):
                p_number = st.number_input(label="段落数", min_value=1, max_value=10, value=1)
                if st.button("确认生成段落"):
                    result = generate_customized_text(locale, "paragraphs", p_number, 0)
                    st.write(result)
            with st.expander(label="客制化生成句子", expanded=False):
                s_number = st.number_input(label="句数", min_value=8, max_value=20, value=10)
                if st.button("确认生成句子"):
                    result = generate_customized_text(locale, "sentences", s_number, 0)
                    st.write(result)
            with st.expander(label="客制化生成文本字符串", expanded=False):
                col1, col2 = st.columns([1, 1])
                with col1:
                    t_number = st.number_input(label="文本字符串数", min_value=1, max_value=10, value=1)
                with col2:
                    max_chars = st.number_input(label="最大词数", min_value=10, max_value=200)
                if st.button("确认生成文本字符串"):
                    result = generate_customized_text(locale, "texts", t_number, max_chars)
                    st.write(result)
            with st.expander(label="客制化生成词组", expanded=False):
                w_number = st.number_input(label="词数", min_value=1, max_value=10)
                if st.button("确认生成词组"):
                    result = generate_customized_text(locale, "words", w_number, 0)
                    st.write(result)




