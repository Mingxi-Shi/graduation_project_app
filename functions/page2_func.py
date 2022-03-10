import streamlit as st

import pandas as pd
import random
import matplotlib.pyplot as plt
import os
from dateutil.parser import parse
from wordcloud import WordCloud, ImageColorGenerator  # 词云库
from streamlit_option_menu import option_menu
from pandas_profiling import ProfileReport  # 报告库
from streamlit_pandas_profiling import st_profile_report  # streamlit报告库
import plotly.express as px
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
from pyg2plot import Plot
import io
import streamlit.components.v1 as components


# ------------------Page2:数据可视化-------------------------------------
def is_date(test_string, fuzzy=False):
    try:
        parse(test_string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False
# ---------------------------------------------------------------------


def generate_html_target(target):
    return io.StringIO(target.render_html()).read()


def dataset_information(df):
    result = [[], []]
    df_columns_name = df.columns.to_list()
    type_of_string_columns_name = []
    type_of_int_columns_name = []
    type_of_float_columns_name = []
    type_of_bool_columns_name = []

    for i in range(len(df.columns)):
        # if df[df_columns_name[i]].dtype == 'object' and is_date(df[df_columns_name[i]][0]) is False:
        if df[df_columns_name[i]].dtype == 'object':
            type_of_string_columns_name.append(df_columns_name[i])
        elif df[df_columns_name[i]].dtype == 'int64':
            type_of_int_columns_name.append(df_columns_name[i])
        elif df[df_columns_name[i]].dtype == 'float64':
            type_of_float_columns_name.append(df_columns_name[i])
        elif df[df_columns_name[i]].dtype == 'bool':
            type_of_bool_columns_name.append(df_columns_name[i])

    result[0] = [df.shape[0], df.shape[1]]  # result[0]赋值
    result[1] = {"string": type_of_string_columns_name,
                 "int": type_of_int_columns_name,
                 "float": type_of_float_columns_name,
                 "bool": type_of_bool_columns_name}

    return result


def generate_chart(df, chart_type):

    # st.write(chart_type)
    if chart_type == "直方图":
        show_histogram(df)
    elif chart_type == "折线图":
        show_line(df)
    elif chart_type == "散点图":
        show_scatter(df)


def show_histogram(df):
    col1, col2 = st.columns([5, 1])
    with col2:
        title = st.text_input(label="图表标题")
        x_data = st.selectbox(label="x轴的列", options=df.columns.to_list())
        y_data = st.selectbox(label="y轴的列", options=[None] + df.columns.to_list())
        color = st.selectbox(label="分类", options=[None] + df.columns.to_list(), index=0)
        pattern_shape = st.selectbox(label="再分类", options=[None] + df.columns.to_list(), index=0)
        opacity = st.slider(label="透明度", min_value=0.0, max_value=1.0, step=0.1, value=1.0, format="%.1f")
        nbins = st.slider(label="条柱的数量", min_value=0, max_value=int(df.shape[0]), value=int(round(df.shape[0])))
        histnorm = st.select_slider(label="y轴的函数", options=[None, 'percent', 'probability', 'density', 'probability density'])
        marginal = st.select_slider(label="外接图", options=[None, 'rug', 'box', 'violin'])
        histfunc = st.select_slider(label="聚合函数(根据Y值)", options=[None, 'count', 'sum', 'avg', 'min', 'max'])
        color_discrete_sequence = st.color_picker(label="柱的颜色", value='#636EFA')
    with col1:
        fig = px.histogram(df, text_auto=True, height=800, hover_data=df.columns,
                           title=title,
                           x=x_data,
                           y=y_data,
                           histfunc=histfunc,
                           opacity=opacity,
                           nbins=nbins,
                           histnorm=histnorm,
                           marginal=marginal,
                           color=color,
                           pattern_shape=pattern_shape,
                           color_discrete_sequence=[color_discrete_sequence]
                           )
        st.plotly_chart(fig, use_container_width=True)


def show_line(df):
    col1, col2 = st.columns([5, 1])
    with col2:
        title = st.text_input(label="图表标题", value="折线图")
        x_data = st.selectbox(label="x轴的列", options=df.columns.to_list())
        y_data = st.selectbox(label="y轴的列", options=df.columns.to_list())
        text_label = st.selectbox(label="点上的标签", options=[None] + df.columns.to_list())
        color = st.selectbox(label="分类", options=[None] + df.columns.to_list(), index=0)
    with col1:
        fig = px.line(df, markers=True,
                      title=title,
                      x=x_data,
                      y=y_data,
                      text=text_label,
                      color=color)
        fig.update_traces(textposition="bottom right")
        st.plotly_chart(fig, use_container_width=True)


def show_scatter(df):
    st.write(1)
    # https://www.jianshu.com/p/41735ecd3f75?utm_campaign=hugo
    # https://plotly.com/python-api-reference/plotly.express.html

def generate_correlated_chart(df):
    columns = df.columns
    s1_choose = st.selectbox("请选择一种数据", columns[0:])
    s2_choose = st.selectbox("请选择一种数据", columns[1:])
    s1 = df[s1_choose].values.tolist()
    s2 = df[s2_choose].values.tolist()
    data = []
    for i in range(df.shape[0]):
        data.append({s1_choose: s1[i], s2_choose: s2[i]})

    line = Plot("Line")
    line.set_options({
        "label": {},
        "data": data,
        "xField": s1_choose,
        "yField": s2_choose,
        "smooth": False,
    })

    line_target = generate_html_target(line)

    # 柱状图
    column = Plot("Column")
    column.set_options({
        "label": {},
        "data": data,
        "xField": s1_choose,
        "yField": s2_choose,
        "seriesField": s1_choose,
        "columnStyle": {
            "radius": [20, 20, 0, 0],
        },
        "slider": {
            "start": 0.0,
            "end": 1.0,
        },
    })

    column_target = generate_html_target(column)

    # 条形图
    bar = Plot("Bar")
    bar.set_options({
        "label": {},
        "data": data,
        "xField": s2_choose,
        "yField": s1_choose,
        "seriesField": s1_choose,
        "legend": {
            "position": 'bottom',
        },
        "slider": {
            "start": 0.0,
            "end": 1.0,
        },
    })

    bar_target = generate_html_target(bar)

    pie = Plot("Pie")
    pie.set_options({
        "label": {},
        "data": data,
        "angleField": s2_choose,
        "colorField": s1_choose,
        "radius": 1,
        "innerRadius": 0.5,
    })
    pie_target = generate_html_target(pie)

    rose = Plot("Rose")
    rose.set_options({
        "label": {},
        "data": data,
        "xField": s1_choose,
        "yField": s2_choose,
        "seriesField": s1_choose,
        "radius": 0.9,
        # 设置 active 状态样式
        "state": {
            "active": {
                "style": {
                    "lineWidth": 0,
                    "fillOpacity": 0.65,
                },
            },
        },
        "legend": {
            "position": 'bottom',
        },
        "interactions": [{"type": 'element-active'}]
    })
    rose_target = generate_html_target(rose)

    area = Plot("Area")
    area.set_options({
        "label": {},
        "data": data,
        "xField": s1_choose,
        "yField": s2_choose,
        "areaStyle": {
            "fill": 'l(270) 0:#ffffff 0.5:#7ec2f3 1:#1890ff',
        },
        "slider": {
            "start": 0.1,
            "end": 0.9,
            "trendCfg": {
                "isArea": True,
            },
        },
        "annotations": [
            {
                "type": 'text',
                "position": ['min', 'median'],
                "content": '中位数',
                "offsetY": 0,
                "style": {
                    "textBaseline": 'bottom',
                },
            },
            {
                "type": 'line',
                "start": ['min', 'median'],
                "end": ['max', 'median'],
                "style": {
                    "stroke": 'red',
                    "lineDash": [2, 2],
                },
            },
        ],

    })
    area_target = generate_html_target(area)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader(s1_choose + "与" + s2_choose + "关系折线图")
        components.html(line_target, height=300)
        components.html("<br>", height=20)
        st.subheader(s1_choose + "与" + s2_choose + "关系玫瑰图")
        components.html(rose_target, height=400)
    with c2:
        st.subheader(s1_choose + "与" + s2_choose + "关系柱状图")
        components.html(column_target, height=300)
        components.html("<br>", height=20)
        st.subheader(s1_choose + "与" + s2_choose + "关系条形图")
        components.html(bar_target, height=300)
    with c3:
        st.subheader(s1_choose + "与" + s2_choose + "关系饼图")
        components.html(pie_target, height=300)
        components.html("<br>", height=20)
        st.subheader(s1_choose + "与" + s2_choose + "关系面积图")
        components.html(area_target, height=300)

