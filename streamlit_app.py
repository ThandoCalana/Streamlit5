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



