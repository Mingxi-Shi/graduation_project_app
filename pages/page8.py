import matplotlib.pyplot as plt

from functions.page8_func import *


# 词云图
def page8():
    st.write("This is page8")

    # 载入文本 1.文本框 2.文本文件txt
    load_text_way = st.radio(label="选择载入文本方式", options=('文本框', '上传文本文件'))
    if load_text_way == '文本框':
        text = st.text_area(label="输入文本", placeholder="Type Here")
    elif load_text_way == '上传文本文件':
        text_file = st.file_uploader("上传文本文件", type=['txt'], key='page8_file_upload_1')
        text = ""
        if text_file is not None:
            text = text_file.getvalue().decode('utf-8')

    if text:
        lyrics = jieba.cut(text)  # 使用jieba分词
        txt = "/".join(lyrics)

        font_names = []
        for files in os.listdir('resources/fonts'):  # 用os库获取文件夹下所有文件名
            font_names.append(files)

        col1, col2, col3 = st.sidebar.columns([1, 1, 4])
        with col1:
            font_color = st.color_picker(label='字体颜色', value='#FFFFFF')
        with col2:
            background_color = st.color_picker(label='背景颜色', value='#000000')
        with col3:
            font_type = st.selectbox(label="字体类型", options=font_names)

        col4, col5 = st.sidebar.columns([2, 1])
        with col4:
            font_max_size = st.slider(label='字体大小', min_value=1, max_value=100, value=50)
        with col5:
            word_margin = st.slider(label='单词间隔', min_value=1, max_value=30, value=2)

        generate_way = st.sidebar.radio(label="选择你要生成的方式", options=('默认', '上传图片作为背景'))
        if generate_way == '默认':
            col6, col7 = st.sidebar.columns([1, 1])
            with col6:
                image_width = st.slider(label='画布宽度', min_value=1, max_value=400, value=400)
            with col7:
                image_height = st.slider(label='画布高度', min_value=1, max_value=400, value=200)
            wc = WordCloud(font_path='resources/fonts/' + font_type, width=image_width, height=image_height, margin=word_margin,
                           background_color=background_color, max_font_size=font_max_size,
                           color_func=lambda *args, **kwargs: font_color)
            wc.generate(txt)  # 导入字体

            fig, ax = plt.subplots()

            plt.imshow(wc)  # 以图片的形式显示词云
            # plt.imshow(wc, interpolation='bilinear')  # 以图片的形式显示词云
            plt.axis("off")  # 关闭图像坐标系
            st.pyplot(fig)  # 显示图片

        elif generate_way == '上传图片作为背景':
            background_image = st.sidebar.file_uploader(label="上传词云图背景", type=['jpg', 'png', 'jpeg'],
                                                        key='page8_file_upload_2')
            if background_image is not None:
                image = Image.open(background_image)  # 初始化自定义背景图
                graph = np.array(image)  # 图像数据化
                wc = WordCloud(font_path='resources/fonts/'+font_type, margin=word_margin, background_color=background_color,
                               max_font_size=80, mask=graph, color_func=lambda *args, **kwargs: font_color)
                image_color = ImageColorGenerator(graph)  # 获得背景图的颜色值
                wc.generate(txt)  # 导入字体

                fig, ax = plt.subplots()
                plt.imshow(wc)  # 以图片的形式显示词云
                # plt.imshow(wc, interpolation='bilinear')  # 以图片的形式显示词云
                plt.axis("off")  # 关闭图像坐标系
                st.pyplot(fig)  # 显示图片