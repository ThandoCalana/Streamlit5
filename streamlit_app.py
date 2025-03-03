import streamlit as st
import pandas as pd
import plotly.express as px



# Define the custom CSS for the background image
#background_image_url = "https://cdn.pixabay.com/photo/2022/07/06/16/25/beautiful-7305547_1280.jpg"  # Replace this with your image URL

# Inject the custom CSS into the Streamlit app
st.markdown(
    f"""
    <style>
        body {{
            background-image: url({"https://cdn.pixabay.com/photo/2022/07/06/16/25/beautiful-7305547_1280.jpg"});
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
page = st.sidebar.radio("Go to", ["Home", "Project Overview", "EDA", "Group Info", "Predictions"])

if page == "Home":
    st.write("Welcome to the Recommender System App!")

elif page == "Project Overview":
    # Main Title
    st.title("Project Overview")

    # Project Description
    st.write("This project focuses on developing a collaborative and content-based recommender system tailored for a collection of anime titles.")

    # Problem Statement
    st.subheader("Problem Statement")
    st.write("Develop a recommender system combining collaborative and content-based approaches to predict users' ratings for unseen anime based on past preferences.")

    # Objectives
    st.subheader("Objectives")
    st.write("Develop a hybrid recommender system that combines collaborative filtering and content-based techniques to accurately predict how users will rate anime titles they have not yet watched, based on their historical viewing preferences and anime characteristics.")



elif page == "EDA":
    st.title("Exploratory Data Analysis")

    # Load Dataset
    anime_data = pd.read_csv("anime.csv")  # Ensure this is the correct file path

    # Display the dataset (Optional)
    st.subheader("Dataset Preview")
    st.write(anime_data.head())

    # Display Descriptive Statistics
    st.subheader("Descriptive Statistics for Categorical Data")
    st.write(anime_data.describe(include='O'))

    # Genre vs Rating Analysis
    st.subheader("Top 10 Genres by Average Rating")

    # Exploding genres into individual rows (Assumes genre is a comma-separated string)
    anime_exploded = anime_data.copy()
    anime_exploded = anime_exploded.dropna(subset=['genre', 'rating'])  # Drop missing values
    anime_exploded['genre'] = anime_exploded['genre'].str.split(', ')  # Split genre into lists
    anime_exploded = anime_exploded.explode('genre')  # Expand into multiple rows

    # Compute average rating per genre
    genre_v_rating = anime_exploded.groupby('genre', as_index=False)['rating'].mean()

    # Select the top 10 genres by frequency
    top_10_genres = anime_exploded['genre'].value_counts().nlargest(10).index
    genre_v_rating = genre_v_rating[genre_v_rating['genre'].isin(top_10_genres)]

    # Sort by rating
    genre_v_rating = genre_v_rating.sort_values(by='rating', ascending=False)

    # Create the bar plot
    fig = px.bar(
        genre_v_rating, 
        x='genre', 
        y='rating', 
        color='genre', 
        text=genre_v_rating['rating'].round(1),
        title="Top 10 Genres by Average Rating",
        labels={'genre': 'Genre', 'rating': 'Average Rating'},
        color_discrete_sequence=px.colors.sequential.Magma
    )

    # Customize layout
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis=dict(gridcolor='lightgray', griddash='dash'), width=1000, height=600)

    # Display the graph in Streamlit
    st.plotly_chart(fig, use_container_width=True)



elif page == "Group Info":
    st.write("## Team Members")
    st.write("- Mpho Moloi : Trello and Streamlit")
    st.write("- Lebogang  Letsoalo : Slidedeck and Streamlit")
    st.write("- Thando Calana : Github Manager")
    st.write("- Thabang Maaphosa")
    st.write("- Thato Mzilikazi")
   

elif page == "Predictions":
    st.write("## Get Recommendations")
    st.write("Feature coming soon!")




