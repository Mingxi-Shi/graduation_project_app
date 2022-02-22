
from functions.page10_func import *


# NLPiffy
def page10():
    st.write("This is page10")
    """ NLP Based App with Streamlit """

    # Title
    st.title("NLPiffy with Streamlit")
    st.subheader("Natural Language Processing On the Go..")

    # Tokenization
    if st.checkbox("Show Tokens and Lemma"):
        st.subheader("Tokenize Your Text")

        message = st.text_area("Enter Text", "Type Here ..")
        if st.button("Analyze"):
            nlp_result = text_analyzer(message)
            st.json(nlp_result)

    # Entity Extraction
    if st.checkbox("Show Named Entities"):
        st.subheader("Analyze Your Text")

        message = st.text_area("Enter Text", "Type Here ..")
        if st.button("Extract"):
            entity_result = entity_analyzer(message)
            st.json(entity_result)

    # Sentiment Analysis
    if st.checkbox("Show Sentiment Analysis"):
        st.subheader("Analyse Your Text")

        message = st.text_area("Enter Text", "Type Here ..")
        if st.button("Analyze"):
            blob = TextBlob(message)
            result_sentiment = blob.sentiment
            st.success(result_sentiment)

    # Summarization
    if st.checkbox("Show Text Summarization"):
        st.subheader("Summarize Your Text")

        message = st.text_area("Enter Text", "Type Here ..")
        summary_options = st.selectbox("Choose Summarizer", ['sumy', 'gensim'])
        if st.button("Summarize"):
            if summary_options == 'sumy':
                st.text("Using Sumy Summarizer ..")
                summary_result = sumy_summarizer(message)
            elif summary_options == 'gensim':
                st.text("Using Gensim Summarizer ..")
                summary_result = summarize(message)
            else:
                st.warning("Using Default Summarizer")
                st.text("Using Gensim Summarizer ..")
                summary_result = summarize(message)

            st.write(summary_result)