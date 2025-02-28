import streamlit as st
import pandas as pd

# Define the custom CSS for the background image
background_image_url = "https://cdn.pixabay.com/photo/2022/07/06/16/25/beautiful-7305547_1280.jpg"  # Replace this with your image URL

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



# Add more content as needed
st.header("Page 1 Content")
st.write("You can add more elements here like text, charts, etc.")
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




