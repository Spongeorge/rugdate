import streamlit as st
from PIL import Image
import gdown
from torchvision import transforms
import requests
from huggingface_hub import get_inference_endpoint

CONSTANT_MEAN_YEAR = 1610.1647039974473
CONSTANT_STD_YER = 389.20546577157154

def pass_to_cv_model(image):
    endpoint = get_inference_endpoint("vit-textile-dating-lube-kkf")

    outputs = endpoint.client.image_classification(image)

    return [(output * CONSTANT_STD_YER) + CONSTANT_MEAN_YEAR for output in outputs]


def main():

    st.title("Rug Date Prediction")

    st.write("Upload an image or select one of the test  images.")

    uploaded_image = st.file_uploader("Upload:", type=["jpg", "jpeg", "png"])

    st.write("Or choose a test image:")
    sample_image_1 = "sample1.jpg"
    sample_image_2 = "sample2.jpg"
    sample_image_3 = "sample3.jpg"



    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Chinese insignia, 1500s"):
            selected_image = Image.open(sample_image_1)
        st.image(Image.open(sample_image_1))
    with col2:
        if st.button("Spanish silk, late 1500s"):
            selected_image = Image.open(sample_image_2)
        st.image(Image.open(sample_image_2))
    with col3:
        if st.button("Italian silk, late 1600s"):
            selected_image = Image.open(sample_image_3)
        st.image(Image.open(sample_image_3))

    # Display uploaded image or selected sample image
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        predicted_dates = pass_to_cv_model(image)
        st.write(f"Predicted Date Range: {predicted_dates}")
    elif 'selected_image' in locals():
        st.image(selected_image, caption="Selected Sample Image", use_column_width=True)
        predicted_dates = pass_to_cv_model(selected_image)
        st.write(f"Predicted Date Range: {predicted_dates}")
    else:
        st.write("No image uploaded or selected.")

if __name__ == "__main__":
    main()
