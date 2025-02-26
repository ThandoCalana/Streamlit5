import streamlit as st
import pandas as pd

st.title("📌 The Recommender System App")
st.sidebar.title("Navigation")

# Sidebar navigation
page = st.sidebar.radio("Go to", ["Home", "EDA", "Group Info", "Predictions"])

if page == "Home":
    st.write("Welcome to the Recommender System App!")

elif page == "EDA":
    st.write("## Exploratory Data Analysis")
    data = pd.read_csv("anime.csv")  # Make sure your file is named correctly
    st.dataframe(data)
    st.write("### Data Summary")
    st.write(data.describe())

elif page == "Group Info":
    st.write("## Team Members")
    st.write("- Mpho Moloi (Trello and streamlit)")
    st.write("- Lebogang  Letsoalo (slidedeck and streamlit)")
    st.write("- Thando Calana (Github Manager)")
    st.write("- Thabang Maaphosa")
    st.write("- Thato Mzilikazi")
   

elif page == "Predictions":
    st.write("## Get Recommendations")
    st.write("Feature coming soon!")

import streamlit as st

def set_background(image_file):
    """Applies a background image using CSS."""
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("https://github.com/LeboL-moriski/Streamlit5/blob/master/Pink%20Black%20Modern%20Outer%20Space%20Presentation.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Load the image and convert it to base64
import base64

def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Streamlit page content
st.title("EDA,Group Info,Predictions")

# Set background only for this page
image_base64 = get_base64_of_image("https://github.com/LeboL-moriski/Streamlit5/blob/master/Pink%20Black%20Modern%20Outer%20Space%20Presentation.jpg")
set_background(image_base64)

st.write("EDA,Group Info,Predictions")


