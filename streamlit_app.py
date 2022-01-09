import pandas as pd
import numpy as np
import streamlit as st
import datetime

from functions import *


def main():
    st.set_page_config(page_title="Shi Mingxi\'s Graduation Project",
                       page_icon=":crown:",
                       layout="wide",
                       initial_sidebar_state="auto",
                       menu_items={'About': None})

    st.sidebar.title("施明希的个人Web")
    menu = st.sidebar.selectbox('选择业务', ('数据处理和分析', '机器学习', '自然语言处理', '案例展示'))
    # st.sidebar.write(menu1)

    if menu == "数据处理和分析":
        menu1_1 = st.sidebar.radio('选择', ('数据处理', '数据分析', '数据挖掘'))
        if menu1_1 == '数据处理':
            page1()
        elif menu1_1 == '数据分析':
            page2()
        elif menu1_1 == '数据挖掘':
            page3()

    elif menu == "机器学习":
        menu1_1 = st.sidebar.radio('选择', ('性别分类', '密码强度检测', '汽车评价', '人脸检测'))
        if menu1_1 == '性别分类':
            page4()
        elif menu1_1 == '密码强度检测':
            page5()
        elif menu1_1 == '汽车评价':
            page6()
        elif menu1_1 == '人脸检测':
            page7()

    elif menu == "自然语言处理":
        menu1_1 = st.sidebar.radio('选择', ('概要和实体检查器', 'NLPiffy', '文档编辑'))
        if menu1_1 == '概要和实体检查器':
            page8()
        elif menu1_1 == 'NLPiffy':
            page9()
        elif menu1_1 == '文档编辑':
            page10()

    elif menu == "案例展示":
        pageExample()

    # st.sidebar.write(menu1_1)

    date = st.sidebar.date_input(
        label="Select a day",
        value=datetime.datetime.now(),
        help="You need to get help?\tContact us")
    # st.sidebar.write(date)

    time = st.sidebar.time_input(
        label="Select an alarm",
        value=datetime.time(8, 00),
        help="You need to get help?\tContact us")
    # st.sidebar.write(time)

    color = st.sidebar.color_picker(
        label="Pick a color",
        value="#00f900",
        help="You need to get help?\tContact us")
    # st.sidebar.write(color)

    st.sidebar.write("BGM func coming soon")
    st.sidebar.button("设置中心")
    st.sidebar.button("帮助中心")


if __name__ == '__main__':
    main()