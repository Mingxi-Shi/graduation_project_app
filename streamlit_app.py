import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components


from pages.page1 import page1
from pages.page2 import page2
from pages.page3 import page3
from pages.page4 import page4
from pages.page5 import page5
from pages.page6 import page6
from pages.page7 import page7
from pages.page8 import page8
from pages.page9 import page9
from pages.page10 import page10
from pages.page11 import page11
from pages.page12 import page12
from pages.page13 import page13


def main():
    st.set_page_config(page_title="Shi Mingxi\'s Graduation Project",
                       page_icon=":crown:",
                       layout="wide",
                       initial_sidebar_state="auto",
                       menu_items={'About': None}
                       )
    st.set_option('deprecation.showPyplotGlobalUse', False)

    hide_menu_style = """
                <style>
                #MainMenu {visibility: hidden;}
                </style>
                """
    st.markdown(hide_menu_style, unsafe_allow_html=True)  # 隐藏网页右上角的菜单

    st.sidebar.title("基于Python+Streamlit的交互式数据可视化网站")
    menu = st.sidebar.selectbox('选择业务', ('数据处理与可视化', '机器学习', '自然语言处理'))

    if menu == "数据处理与可视化":
        with st.sidebar:
            menu_1 = option_menu(menu_title="数据处理与可视化", options=["数据预处理", "数据可视化", "在线编辑"],
                                 icons=["hypnotize", "hypnotize", "hypnotize", "hypnotize"], menu_icon="list-task",
                                 default_index=0, orientation="vertical")
        if menu_1 == '数据预处理':
            page1()
        elif menu_1 == '数据可视化':
            page2()
        elif menu_1 == '在线编辑':
            page3()

    elif menu == "机器学习":
        # menu_2 = st.sidebar.radio('选择', ('性别分类', '密码强度检测', '假数据生成', '人脸检测'))
        with st.sidebar:
            menu_2 = option_menu(menu_title="机器学习", options=["性别分类", "密码强度检测", "假数据生成", "人脸检测"],
                                 icons=["hypnotize", "hypnotize", "hypnotize", "hypnotize"], menu_icon="list-task",
                                 default_index=0, orientation="vertical")
        if menu_2 == '性别分类':
            page4()
        elif menu_2 == '密码强度检测':
            page5()
        elif menu_2 == '假数据生成':
            page6()
        elif menu_2 == '人脸检测':
            page7()

    elif menu == "自然语言处理":
        # menu_3 = st.sidebar.radio('选择', ('词云图', '概要和实体检查器', 'NLPiffy', '提取电话和电子邮箱', '情感分析', '百度API'))
        with st.sidebar:
            menu_3 = option_menu(menu_title="自然语言处理", options=["词云图", "概要和实体检查器", "NLPiffy", "提取电话和电子邮箱", "情感分析", "百度API"],
                                 icons=["hypnotize", "hypnotize", "hypnotize", "hypnotize", "hypnotize", "hypnotize", "hypnotize"], menu_icon="list-task",
                                 default_index=0, orientation="vertical")
        if menu_3 == '词云图':
            page8()
        if menu_3 == '概要和实体检查器':
            page9()
        elif menu_3 == 'NLPiffy':
            page10()
        elif menu_3 == '提取电话和电子邮箱':
            page11()
        elif menu_3 == '情感分析':
            page12()
        elif menu_3 == '百度API':
            page13()

    # date = st.sidebar.date_input(
    #    label="Select a day",
    #    value=datetime.datetime.now(),
    #    help="You need to get help?\tContact us")

    # time = st.sidebar.time_input(
    #    label="Select an alarm",
    #    value=datetime.time(8, 00),
    #    help="You need to get help?\tContact us")

    # color = st.sidebar.color_picker(
    #    label="Pick a color",
    #    value="#00f900",
    #    help="You need to get help?\tContact us")

    # st.sidebar.write("BGM func coming soon")
    # st.sidebar.button("设置中心")
    # st.sidebar.button("帮助中心")


if __name__ == '__main__':
    main()
