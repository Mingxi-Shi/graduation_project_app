
from functions.page13_func import *


def page13():

    """ APPID AK SK """
    APP_ID = '25633539'
    API_KEY = '6LrhCx6p0S7Qk3R7OlBfsoFR'
    SECRET_KEY = 'KeAboYvmlv0qD6K8r6fMN6VFKem1bXdL'
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

    page13_menu = st.sidebar.selectbox(label="选择", options=("评论观点抽取", "新闻摘要", "文本纠错", "文章分类",
                                                            "文章标签", "情感倾向分析", "对话情绪识别"))

    if page13_menu == "评论观点抽取":
        input_text = st.text_area(label="输入评论文本", max_chars=5000)
        if input_text and st.button("开始抽取"):
            result = client.commentTag(input_text)
            for i in result["items"]:
                st.write("属性词：", i["prop"])
                st.write("描述词：", i["adj"])
                st.write("情感极性（0表示消极，1表示中性，2表示积极）：", i["sentiment"])
                st.write("短句摘要：", i["abstract"])
                st.write("--------------------")

    elif page13_menu == "新闻摘要":
        input_text = st.text_area(label="新闻内容", max_chars=3000)
        st.write("该文本的字数为：", len(input_text))
        max_summary_length = st.number_input(label='摘要结果最大字数', value=len(input_text))
        if input_text and st.button("开始摘要"):
            result = client.newsSummary(input_text, max_summary_len=max_summary_length)
            st.write("摘要结果：", result["summary"])
            pyperclip.copy(result["summary"])
            st.info("已自动复制至剪切板")

    elif page13_menu == "文本纠错":
        input_text = st.text_area(label="文本纠错", max_chars=240)
        st.write("该文本的字数为：", len(input_text))
        if input_text and st.button("开始纠错"):
            result = client.ecnet(input_text)
            count = 0
            for i in result["item"]["vec_fragment"]:
                st.error("检测到错误文本：" + i["ori_frag"])
                st.success("修改为：" + i["correct_frag"])
                count += 1
            st.info("总计%d处错误" % count)
            st.write("纠错后结果：", result["item"]["correct_query"])
            st.write("模型置信度：", result["item"]["score"])
            pyperclip.copy(result["item"]["correct_query"])
            st.info("已自动复制至剪切板")

    elif page13_menu == "文章分类":
        input_title_text = st.text_input(label="文章标题", max_chars=40)
        input_content_text = st.text_area(label="文章内容", max_chars=math.floor(65535/2))

        if input_title_text and input_content_text and st.button("开始分类"):
            result = client.topic(title=input_title_text, content=input_content_text)

            whole_dict = {result["item"]["lv1_tag_list"][0]["tag"]: result["item"]["lv1_tag_list"][0]["score"]}
            for i in range(len(result["item"]["lv2_tag_list"])):
                whole_dict[result["item"]["lv2_tag_list"][i]["tag"]] = result["item"]["lv2_tag_list"][i]["score"]
            i = 1
            for keys, values in whole_dict.items():
                st.write("文章的第", i, "分类：", keys, " 得分为：", values)
                i += 1

    elif page13_menu == "文章标签":
        input_title_text = st.text_input(label="文章标题", max_chars=40)
        input_content_text = st.text_area(label="文章内容", max_chars=math.floor(65535 / 2))

        if input_title_text and input_content_text and st.button("开始标签"):
            result = client.keyword(input_title_text, input_content_text)
            # st.write(result)

            whole_dict = {}
            for i in range(len(result["items"])):
                whole_dict[result["items"][i]["tag"]] = result["items"][i]["score"]
            # st.write(whole_dict)
            i = 1
            for keys, values in whole_dict.items():
                st.write("文章的第", i, "标签：", keys, " 得分为：", values)
                i += 1

    elif page13_menu == "情感倾向分析":
        input_text = st.text_area(label="单一主观文本", max_chars=1024)

        if input_text and st.button("开始分析"):
            result = client.sentimentClassify(input_text)
            # st.write(result)
            p1, p2 = st.columns([5,5])
            with p1:
                plt.rcParams['font.sans-serif'] = ['Simhei']
                probity = [result["items"][0]["positive_prob"], result["items"][0]["negative_prob"]]
                fig, ax = plt.subplots()

                plt.pie(x=probity, labels=["积极", "消极"], autopct='%.2f')
                plt.legend(loc="upper right")
                st.pyplot(fig=plt)
            with p2:
                if result["items"][0]["sentiment"] == 0:
                    st.info("负向:worried:")
                elif result["items"][0]["sentiment"] == 1:
                    st.info("中性:expressionless:")
                elif result["items"][0]["sentiment"] == 2:
                    st.info("正向:smile:")
                st.info("置信度：" + str(result["items"][0]["confidence"]))

    elif page13_menu == "对话情绪识别":
        input_text = st.text_area(label="待识别情感文本", max_chars=256)

        if input_text and st.button("开始识别"):
            result = client.emotion(input_text)
            # st.write(result)
            p1, p2, p3 = st.columns([1, 7, 7])
            with p1:
                if result["items"][0]["label"] == "pessimistic":
                    load_images('resources/images/pessimistic.jpg')
                elif result["items"][0]["label"] == "neutral":
                    load_images('resources/images/neutral.jpg')
                else:
                    load_images('resources/images/optimistic.jpg')
            with p2:
                st.success("参考回复话术：" + result["items"][0]["replies"][0])
            with p3:
                st.info("情绪一级分类标签：" + result["items"][0]["label"] + "，概率：" + str(result["items"][0]["prob"]))
                st.info("情绪二级分类标签：" + result["items"][0]["subitems"][0]["label"] + "，概率：" + str(result["items"][0]["subitems"][0]["prob"]))


