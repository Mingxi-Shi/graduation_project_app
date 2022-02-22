
from functions.page5_func import *


# 密码强度检测
def page5():
    st.write("This is page5")

    activities = ["Password Generation", "Password Strength Classifier"]
    choice = st.sidebar.selectbox("Select Activity", activities)

    if choice == "Password Generation":
        st.subheader("Generate Random Password")

        pwd_length = st.number_input("输入生成密码的长度", min_value=8, max_value=25)

        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            is_have_uppercase = st.checkbox(label="ABCDEFGHIJKLMNOPQRSTUVWXYZ", key="upper")
        with col2:
            is_have_lowercase = st.checkbox(label="abcdefghijklmnopqrstuvwxyz", key="lower")
        with col3:
            is_have_digit = st.checkbox(label="0123456789")
        with col4:
            is_have_punctuation = st.checkbox(label="!\"#$%&'()*+,-./:;<=>?@[]^_`{|}~")

        if is_have_uppercase or is_have_lowercase or is_have_digit or is_have_punctuation:
            if st.button("开始生成"):
                custom_password = password_gen(pwd_length, is_have_uppercase, is_have_lowercase, is_have_digit, is_have_punctuation)
                pyperclip.copy(custom_password)
                st.write(custom_password)
                st.write("已自动复制至粘贴板")

    elif choice == "Password Strength Classifier":
        st.subheader("Classifying Password with ML")

        password = st.text_input("Enter Password", placeholder="Type Here")

        if password:

            st.write("分数：", passwordstrength.passwordmeter.PasswordStrength(password).strength())
            st.write("强度：", passwordstrength.passwordmeter.PasswordStrength(password).rating())