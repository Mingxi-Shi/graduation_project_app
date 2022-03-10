
from functions.page7_func import *


# 人脸检测
def page7():
    st.title("人脸检测")
    image_file = st.sidebar.file_uploader("上传一张含有人脸的图片", type=['jpg', 'png', 'jpeg'], key='page7_file_upload')
    if image_file is not None:
        original_image = Image.open(image_file)
        st.text("原始图像")
        st.image(original_image)
        enhance_type = st.sidebar.radio("增强类型",
                                        ["原始图像", "灰度", "对比度", "亮度", "模糊度"])

        if enhance_type == '灰度':
            rgb_array_img = np.array(original_image.convert('RGB'))
            img = cv2.cvtColor(rgb_array_img, 1)
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            st.text("处理灰度后:")
            st.image(gray_img)

        elif enhance_type == '对比度':
            c_rate = st.sidebar.slider("Contrast", 0.5, 3.5)
            enhancer = ImageEnhance.Contrast(original_image)
            contrast_img = enhancer.enhance(c_rate)
            st.text("处理对比度后:")
            st.image(contrast_img)

        elif enhance_type == '亮度':
            c_rate = st.sidebar.slider("Brightness", 0.5, 3.5)
            enhancer = ImageEnhance.Brightness(original_image)
            brightness_img = enhancer.enhance(c_rate)
            st.text("处理亮度后:")
            st.image(brightness_img)

        elif enhance_type == '模糊度':
            rgb_array_img = np.array(original_image.convert('RGB'))
            blur_rate = st.sidebar.slider("Brightness", 0.5, 3.5)
            img = cv2.cvtColor(rgb_array_img, 1)
            blur_img = cv2.GaussianBlur(img, (11, 11), blur_rate)
            st.text("处理模糊度后:")
            st.image(blur_img)

        # Face Detection
        feature = ["人脸", "笑容", "眼睛", "黑白简笔化", "卡通化"]
        feature_choice = st.sidebar.selectbox("功能选择", feature)
        if st.button("开始检测"):
            if feature_choice == '人脸':
                result_img, result_faces = detect_faces(original_image)
                st.image(result_img)
                st.success("找到 {} 张人脸".format(len(result_faces)))

            elif feature_choice == '笑容':
                result_img = detect_smiles(original_image)
                st.image(result_img)

            elif feature_choice == '眼睛':
                result_img = detect_eyes(original_image)
                st.image(result_img)

            elif feature_choice == '黑白简笔化':
                result_canny = cannize_image(original_image)
                st.image(result_canny)

            elif feature_choice == '卡通化':
                result_img = cartonize_image(original_image)
                st.image(result_img)


