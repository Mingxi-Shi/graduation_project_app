
from functions.page4_func import *

import gender_ai as ga


# 性别分类
def page4():
    st.write("This is page5")
    st.title("Gender Classifier ML App")
    html_temp = """
        <div style="background-color:tomato;padding:5px;">
        <h3> Streamlit ML App </h3>
        </div>
        """

    st.markdown(html_temp, unsafe_allow_html=True)
    name = st.text_input(label="Enter an English name and predict whether it is male or female through AI",
                         placeholder="Type Here")
    if st.button("Classify"):
        result = ga.predict(name)
        if result == 'Girl':
            c_image = 'resources/images/female.png'
        elif result == 'Boy':
            c_image = 'resources/images/male.png'
        st.success("Name {}, was classified as {}".format(name.title(), result))
        load_images(c_image)