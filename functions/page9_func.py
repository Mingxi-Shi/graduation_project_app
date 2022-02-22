
import streamlit as st

# Sumy Summary Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

import spacy
from spacy import displacy
nlp = spacy.load("en_core_web_sm")

from gensim.summarization import summarize

# --------Page9:summarizer and entity checker总结和实体检查-----------------
# Function for Sumy Summarization
def sumy_summarizer(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer("chinese"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document,3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result


# Fetch Text From Url
@st.cache
def get_text(raw_url):
    page = urlopen(raw_url)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text


def analyze_text(text):
    return nlp(text)
# -----------------------------------------------------------------------
