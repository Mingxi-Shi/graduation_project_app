
from functions.page7_func import *


# 人脸检测
def page7():
    # st.write("This is page7")

    st.title("人脸检测")
    image_file = st.file_uploader("上传一张含有人脸的图片", type=['jpg', 'png', 'jpeg'], key='page7_file_upload')
    if image_file is not None:
        original_image = Image.open(image_file)
        st.text("Original Image")
        st.image(original_image)
        enhance_type = st.sidebar.radio("Enhance Type",
                                        ["Original", "Gray-Scale", "Contrast", "Brightness", "Blurring"])

        if enhance_type == 'Gray-Scale':
            rgb_array_img = np.array(original_image.convert('RGB'))
            img = cv2.cvtColor(rgb_array_img, 1)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            st.text("after processing Gray-Scale:")
            st.image(gray_img)

        elif enhance_type == 'Contrast':
            c_rate = st.sidebar.slider("Contrast", 0.5, 3.5)
            enhancer = ImageEnhance.Contrast(original_image)
            contrast_img = enhancer.enhance(c_rate)
            st.text("after processing Contrast:")
            st.image(contrast_img)

        elif enhance_type == 'Brightness':
            c_rate = st.sidebar.slider("Brightness", 0.5, 3.5)
            enhancer = ImageEnhance.Brightness(original_image)
            brightness_img = enhancer.enhance(c_rate)
            st.text("after processing Brightness:")
            st.image(brightness_img)

        elif enhance_type == 'Blurring':
            rgb_array_img = np.array(original_image.convert('RGB'))
            blur_rate = st.sidebar.slider("Brightness", 0.5, 3.5)
            img = cv2.cvtColor(rgb_array_img, 1)
            blur_img = cv2.GaussianBlur(img, (11, 11), blur_rate)
            st.text("after processing Blurring:")
            st.image(blur_img)

        # Face Detection
        feature = ["Faces", "Smiles", "Eyes", "Cannize", "Cartonize"]
        feature_choice = st.sidebar.selectbox("Find Features", feature)
        if st.button("Process"):
            if feature_choice == 'Faces':
                result_img, result_faces = detect_faces(original_image)
                st.image(result_img)
                st.success("Found {} faces".format(len(result_faces)))

            elif feature_choice == 'Smiles':
                result_img = detect_smiles(original_image)
                st.image(result_img)

            elif feature_choice == 'Eyes':
                result_img = detect_eyes(original_image)
                st.image(result_img)

            elif feature_choice == 'Cartonize':
                result_img = cartonize_image(original_image)
                st.image(result_img)

            elif feature_choice == 'Cannize':
                result_canny = cannize_image(original_image)
                st.image(result_canny)