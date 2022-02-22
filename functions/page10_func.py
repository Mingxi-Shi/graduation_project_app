
import streamlit as st

# Sumy Summary Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

import spacy
from spacy import displacy
# nlp = spacy.load("en_core_web_sm")

# NLP Pkgs
from textblob import TextBlob

from gensim.summarization import summarize

#
# # ----------------------Page10:NLPiffy自然语言处理--------------------------
# # Sumy Summarization
# def sumy_summarizer(docx):
#     parser = PlaintextParser.from_string(docx, Tokenizer("chinese"))
#     lex_summarizer = LexRankSummarizer()
#     summary = lex_summarizer(parser.document, 3)
#     summary_list = [str(sentence) for sentence in summary]
#     result = ' '.join(summary_list)
#     return result
#
#
# # Function For Analysing Tokens and Lemma
# @st.cache
# def text_analyzer(my_text):
#     docx = nlp(my_text)
#     # tokens = [ token.text for token in docx]
#     allData = [('"Token":{},\n"Lemma":{}'.format(token.text, token.lemma_)) for token in docx]
#     return allData
#
#
# # Function For Extracting Entities
# @st.cache
# def entity_analyzer(my_text):
#     docx = nlp(my_text)
#     tokens = [token.text for token in docx]
#     entities = [(entity.text, entity.label_) for entity in docx.ents]
#     allData = ['"Token":{},\n"Entities":{}'.format(tokens, entities)]
#     return allData
# # -----------------------------------------------------------------------
