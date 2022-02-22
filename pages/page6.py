
from functions.page6_func import *


# 假数据生成
def page6():
    st.write("This is page6")
    st.title("Fake Data Generator")

    localized_providers = ["ar_AA", "ar_EG", "ar_JO", "ar_PS", "ar_SA", "bg_BG", "bs_BA", "cs_CZ", "de", "de_AT",
                           "de_CH", "de_DE", "dk_DK", "el_CY", "el_GR", "en", "en_AU", "en_CA", "en_GB", "en_IE",
                           "en_IN", "en_NZ", "en_PH", "en_TH", "en_US", "es", "es_CA", "es_ES", "es_MX", "et_EE",
                           "fa_IR", "fi_FI", "fil_PH", "fr_CA", "fr_CH", "fr_FR", "fr_QC", "he_IL", "hi_IN",
                           "hr_HR", "hu_HU", "hy_AM", "id_ID", "it_CH", "it_IT", "ja_JP", "ka_GE", "ko_KR", "la",
                           "lb_LU", "lt_LT", "lv_LV", "mt_MT", "ne_NP", "nl_BE", "nl_NL", "no_NO", "or_IN", "pl_PL",
                           "pt_BR", "pt_PT", "ro_RO", "ru_RU", "sk_SK", "sl_SI", "sv_SE", "ta_IN", "th", "th_TH",
                           "tl_PH", "tr_TR", "tw_GH", "uk_UA", "zh_CN", "zh_TW"]

    menu = ["Home", "Customize"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.subheader("Home")
        number_to_gen = st.sidebar.number_input("Number", 10, 5000)
        locale = st.sidebar.multiselect("Select Locale", localized_providers, default="en_US")
        dataformat = st.sidebar.selectbox("Save Data As", ["csv", "json"])
        df = generate_locale_profile(number_to_gen, locale)
        st.dataframe(df)
        with st.expander("📩: Download"):
            make_downloadable_df_format(df, dataformat)

    elif choice == "Customize":
        st.subheader("Customize Your Fields")
        # Locale Providers For Faker Class

        locale = st.sidebar.multiselect("Select Locale", localized_providers, default="en_US")

        profile_options_list = ['username', 'name', 'sex', 'address', 'mail', 'birthdate''job', 'company', 'ssn',
                                'residence', 'current_location', 'blood_group', 'website']
        profile_fields = st.sidebar.multiselect("Fields", profile_options_list, default='username')

        number_to_gen = st.sidebar.number_input("Number", 10, 10000)
        dataformat = st.sidebar.selectbox("Save Data As", ["csv", "json"])

        # Initialize Faker Class
        custom_fake = Faker(locale)
        data = [custom_fake.profile(fields=profile_fields) for i in range(number_to_gen)]
        df = pd.DataFrame(data)

        # View As Dataframe
        st.dataframe(df)

        # View as JSON
        with st.expander("🔍: View JSON "):
            st.json(data)

        with st.expander("📩: Download"):
            make_downloadable_df_format(df, dataformat)