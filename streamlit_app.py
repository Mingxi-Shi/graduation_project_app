import streamlit as st

# from functions import *

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


def main():
    st.set_page_config(page_title="Shi Mingxi\'s Graduation Project",
                       page_icon=":crown:",
                       layout="wide",
                       initial_sidebar_state="auto",
                       menu_items={'About': None})
    st.sidebar.title("施明希的个人Web")
    menu = st.sidebar.selectbox('选择业务', ('数据处理与可视化分析', '机器学习', '自然语言处理', '案例展示'))

    if menu == "数据处理与可视化分析":
        menu1_1 = st.sidebar.radio('选择', ('数据处理', '数据可视化', '数据挖掘'))
        if menu1_1 == '数据处理':
            page1()
        elif menu1_1 == '数据可视化':
            page2()
        elif menu1_1 == '数据挖掘':
            page3()

    elif menu == "机器学习":
        menu1_1 = st.sidebar.radio('选择', ('性别分类', '密码强度检测', '假数据生成', '人脸检测'))
        if menu1_1 == '性别分类':
            page4()
        elif menu1_1 == '密码强度检测':
            page5()
        elif menu1_1 == '假数据生成':
            page6()
        elif menu1_1 == '人脸检测':
            page7()

    elif menu == "自然语言处理":
        menu1_1 = st.sidebar.radio('选择', ('词云图', '概要和实体检查器', 'NLPiffy', '提取电话和电子邮箱', '情感分析'))
        if menu1_1 == '词云图':
            page8()
        if menu1_1 == '概要和实体检查器':
            page9()
        elif menu1_1 == 'NLPiffy':
            page10()
        elif menu1_1 == '提取电话和电子邮箱':
            page11()
        elif menu1_1 == '情感分析':
            page12()

    elif menu == "案例展示":
        # pageExample()
        st.write("..................")

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
