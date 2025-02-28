import streamlit as st
import pandas as pd

# Define the custom CSS for the background image
background_image_url = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fpixabay.com%2Fphotos%2Fbeautiful-deep-space-cosmic-7305547%2F&psig=AOvVaw177nnlX5t2NhW2n1sueR4Z&ust=1740826323155000&source=images&cd=vfe&opi=89978449&ved=0CBAQjRxqFwoTCOD4sMmZ5osDFQAAAAAdAAAAABAE" 

# Inject the custom CSS into the Streamlit app
st.markdown(
    f"""
    <style>
        body {{
            background-image: url({background_image_url});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Example content for the Streamlit app
st.title("Streamlit App with Background Image")
st.write("This page has a custom background image. Add your content below!")

# Add more content as needed
st.header("Page 1 Content")
st.write("You can add more elements here like text, charts, etc.")



# Load the image and convert it to base64
import base64

def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:"Pink Black Modern Outer Space Presentation.jpg"
    return base64.b64encode(Pink Black Modern Outer Space Presentation.jpg"")).decode()

# Streamlit page content
st.title("EDA,Group Info,Predictions")

# Set background only for this page
image_base64 = get_base64_of_image("Pink Black Modern Outer Space Presentation.jpg")
set_background(image_base64)

st.write("EDA,Group Info,Predictions")
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




