
from functions.page11_func import *


# 提取电话和电子邮箱
def page11():
    st.write("This is page12")
    st.title("Email Extractor App")
    menu = ["Single Extractor", "Bulk Extractor"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Single Extractor":
        st.subheader("Extract A Single Term")
        text = st.text_area("Paste Text Here")
        task_option = st.sidebar.selectbox("Task", ["Emails", "URLS", "Phonenumbers"])
        if text:
            if st.button("Extract"):

                if task_option == "URLS":
                    results = nfx.extract_urls(text)
                elif task_option == "Phonenumbers":
                    results = nfx.extract_phone_numbers(text)
                else:
                    results = nfx.extract_emails(text)

                st.write(results)

                with st.expander("Results As DataFrame"):
                    result_df = pd.DataFrame({'Results': results})
                    st.dataframe(result_df)
                    make_downloadable(result_df, task_option)

    elif choice == "Bulk Extractor":
        st.subheader("Bulk Extractor")
        text = st.text_area("Paste Text Here")
        tasks_list = ["Emails", "URLS", "Phonenumbers"]
        task_option = st.sidebar.multiselect("Task", tasks_list, default="Emails")
        task_mapper = {"Emails": nfx.extract_emails(text), "URLS": nfx.extract_urls(text)
            , "Phonenumbers": nfx.extract_phone_numbers(text)}
        if text:
            all_results = []
            for task in task_option:
                result = task_mapper[task]
                # st.write(result)
                all_results.append(result)
            st.write(all_results)

            with st.expander("Results As DataFrame"):
                result_df = pd.DataFrame(all_results).T
                result_df.columns = task_option
                st.dataframe(result_df)
                make_downloadable_df(result_df)