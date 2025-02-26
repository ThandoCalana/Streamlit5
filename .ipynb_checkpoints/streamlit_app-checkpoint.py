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

# Embed HTML for video background
st.markdown("""
    <style>
        /* Set the video background to fill the whole page */
        .video-background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: -1;
        }
        /* Make the content appear above the video */
        .content {
            position: relative;
            z-index: 1;
        }
    </style>
    <video autoplay loop muted class="video-background">
        <source src="https://motionbgs.com/media/5476/sung-jin-woo-purple.960x540.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
""", unsafe_allow_html=True)

# Now your regular Streamlit content will appear above the video
st.title("Streamlit App with Video Background")
st.write("This is a Streamlit app with a video in the background!")




