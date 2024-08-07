import streamlit as st
from PIL import Image
import requests
import io
import json
import time


CONSTANT_MEAN_YEAR = 1610.1647039974473
CONSTANT_STD_YEAR = 389.20546577157154

API_URL = "https://zc4u7gor8e17vbi9.us-east-1.aws.endpoints.huggingface.cloud"

headers = {
	"Accept" : "application/json",
	"Content-Type": "image/jpeg"
}

parameters = {
    "function_to_apply": "none"
}

def pass_to_cv_model(image):

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    response = requests.post(API_URL, headers=headers, params=parameters, data=img_byte_arr)
    content = json.loads(response.content)

    outputs = [(x['score'] * CONSTANT_STD_YEAR) + CONSTANT_MEAN_YEAR for x in content]

    outputs = [int("{:.0f}".format(output)) for output in outputs]

    return f"{outputs[1]}-{outputs[0]}"


def main():

    if not check_endpoint_status():
        spin_up_endpoint()
        wait_for_endpoint()

    st.title("Rug Date Prediction")

    st.write("Upload an image or select one of the test  images.")

    if 'selected_image' not in st.session_state:
        st.session_state.selected_image = None

    st.session_state.uploaded_image = st.file_uploader("Upload:", type=["jpg", "jpeg", "png"])

    st.write("Or choose a test image:")
    sample_image_1 = "sample1.jpg"
    sample_image_2 = "sample2.jpg"
    sample_image_3 = "sample3.jpg"

    selected_image = None

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Egyptian Textile, 500-700"):
            st.session_state.selected_image = Image.open(sample_image_1)
        st.image(Image.open(sample_image_1))
    with col2:
        if st.button("Iranian Khorjin, 1870-1900"):
            st.session_state.selected_image = Image.open(sample_image_2)
        st.image(Image.open(sample_image_2))
    with col3:
        if st.button("Italian Silk, late 1600s"):
            st.session_state.selected_image = Image.open(sample_image_3)
        st.image(Image.open(sample_image_3))

    image = Image.open(st.session_state.uploaded_image) if st.session_state.uploaded_image else st.session_state.selected_image
    if image:
        st.image(image, caption="Selected Image", use_column_width=True)
        if st.button("Date this textile"):

            with st.spinner("Running inference..."):
                predicted_dates = pass_to_cv_model(image)

            st.write(f"Predicted Date Range: {predicted_dates}")
    else:
        st.write("No image uploaded or selected.")

def check_endpoint_status():
    """Check if the endpoint is available."""
    try:
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        st.error(f"Error checking endpoint status: {e}")
        return False

def spin_up_endpoint():
    """Send a dummy request to spin up the endpoint."""
    dummy_data = {
        "inputs": "This is a test input to spin up the instance."
    }
    try:
        response = requests.post(API_URL, headers=headers, json=dummy_data)
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        st.error(f"Error spinning up endpoint: {e}")
        return False

def wait_for_endpoint():
    """Wait until the endpoint is fully available."""
    with st.spinner("Waiting for the endpoint to be ready..."):
        while not check_endpoint_status():
            time.sleep(5)
    st.write("Endpoint is ready.")

if __name__ == "__main__":
    main()
