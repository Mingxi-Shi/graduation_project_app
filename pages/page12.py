
from functions.page12_func import *


# 情感分析
def page12():
    st.write("This is page12")

    """Sentiment Analysis Emoji App """

    st.title("Sentiment Analysis Emoji App")

    activities = ["Sentiment", "Text Analysis on URL"]
    choice = st.sidebar.selectbox("Choice", activities)

    if choice == 'Sentiment':
        st.subheader("Sentiment Analysis")
        st.write(emoji.emojize('Everyone :red_heart: Streamlit ', use_aliases=True))
        raw_text = st.text_area("Enter Your Text", "Type Here")
        if st.button("Analyze"):
            blob = TextBlob(raw_text)
            result = blob.sentiment.polarity
            if result > 0.0:
                custom_emoji = ':smile:'
                st.write(emoji.emojize(custom_emoji, use_aliases=True))
            elif result < 0.0:
                custom_emoji = ':disappointed:'
                st.write(emoji.emojize(custom_emoji, use_aliases=True))
            else:
                st.write(emoji.emojize(':expressionless:', use_aliases=True))
            st.info("Polarity Score is:: {}".format(result))

    if choice == 'Text Analysis on URL':
        st.subheader("Analysis on Text From URL")
        raw_url = st.text_input("Enter URL Here", "Type here")
        text_preview_length = st.slider("Length to Preview", 50, 100)
        if st.button("Analyze"):
            if raw_url != "Type here":
                result = get_text(raw_url)
                blob = TextBlob(result)
                len_of_full_text = len(result)
                len_of_short_text = round(len(result) / text_preview_length)
                st.success("Length of Full Text::{}".format(len_of_full_text))
                st.success("Length of Short Text::{}".format(len_of_short_text))
                st.info(result[:len_of_short_text])
                c_sentences = [sent for sent in blob.sentences]
                c_sentiment = [sent.sentiment.polarity for sent in blob.sentences]

                new_df = pd.DataFrame(zip(c_sentences, c_sentiment), columns=['Sentence', 'Sentiment'])
                st.dataframe(new_df)

    with st.expander(label="使用TextBlob包"):
        text = "I am so happy."
        blob = TextBlob(text)

        st.write(blob.sentiment)

    with st.expander(label="使用SnowNLP包"):
        a = st.text_area(label="输入文本进行情感分析")
        if a:
            b = SnowNLP(a)
            st.write(b.words)
            st.write(b.tags)
            st.write(b.sentiments)
    with st.expander(label="使用百度AI开放平台的情感倾向分析API"):
        """ 你的 APPID AK SK """
        APP_ID = '25633539'
        API_KEY = '6LrhCx6p0S7Qk3R7OlBfsoFR'
        SECRET_KEY = 'KeAboYvmlv0qD6K8r6fMN6VFKem1bXdL'

        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
        text = "以前约过一个电子系妹子，之前和妹子关系都挺好的约出去一切也很正常，直到不知怎么问起GPA。 我说我GPA不行，只有多少多少。(大概略高于平均吧） 她哦了一声，说她有多少多少（反正比我高很多，她貌似是他们系前几名） 从此以后她再也没理过我。 "
        result = client.sentimentClassify(text)
        st.write(result)
