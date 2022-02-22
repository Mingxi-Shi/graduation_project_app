
import streamlit as st

import passwordstrength.passwordmeter
import pyperclip
import string
import random


# -------------Page5:password Classifier密码强度检测------------------------
def password_gen(length, uppercase, lowercase, digit, punctuation):
    characters = ""
    if uppercase:
        characters += string.ascii_uppercase
    if lowercase:
        characters += string.ascii_lowercase
    if digit:
        characters += string.digits
    if punctuation:
        characters += string.punctuation
    # characters = string.digits + string.ascii_letters + string.punctuation
    generated_pswd = "".join(random.choice(characters) for x in range(length))
    return generated_pswd
# -----------------------------------------------------------------------
