import streamlit as st
from PIL import Image
import gdown
import torch
import timm
from torchvision import transforms

inference_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5670, 0.5327, 0.4973], std=[0.2165, 0.2195, 0.2175])
    ])

url = 'https://drive.google.com/uc?id=1-4A9w60IkPSxsMkEiT3GYtr1RgFBhvD1'

    output = 'model_state_dict.pth'

    gdown.download(url, output, quiet=False)

    model = timm.create_model('vit_huge_patch14_224.orig_in21k', pretrained=True)

    model.head = torch.nn.Linear(1280, 2)

    model.load_state_dict(state_dict)

def pass_to_cv_model(image):
    # Placeholder function that simulates model prediction
    # Replace with your actual model prediction logic
    return model(inference_transforms(image))

def main():

    st.title("Rug Date Prediction")

    st.write("Upload an image or select one of the test  images.")

    uploaded_image = st.file_uploader("Upload:", type=["jpg", "jpeg", "png"])

    st.write("Or choose a test image:")
    sample_image_1 = "sample1.jpg"
    sample_image_2 = "sample2.jpg"
    sample_image_3 = "sample3.jpg"

    size = (224, 224)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Chinese insignia, 1500s"):
            selected_image = Image.open(sample_image_1)
        st.image(Image.open(sample_image_1).resize(size))
    with col2:
        if st.button("Spanish silk, late 1500s"):
            selected_image = Image.open(sample_image_2)
        st.image(Image.open(sample_image_2).resize(size))
    with col3:
        if st.button("Italian silk, late 1600s"):
            selected_image = Image.open(sample_image_3)
        st.image(Image.open(sample_image_3).resize(size))

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
