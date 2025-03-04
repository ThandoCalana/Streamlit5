import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import gzip
import base64

# Function to set video background
def set_video_background(video_file):
    video_url = f"data:video/mp4;base64,{base64.b64encode(open(video_file, 'rb').read()).decode()}"
    st.markdown(
        f"""
        <style>
        @keyframes videoBG {{
            from {{opacity: 1;}}
            to {{opacity: 1;}}
        }}
        
        .stApp {{
            background: url({video_url}) no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
# Define a function for collaborative filtering using the pickled SVD model
def collaborative_filtering(user_id, anime_df, svd_model):
    # Predict ratings for all anime for the given user using the SVD model
    anime_ids = anime_df['anime_id'].unique()
    predicted_ratings = []

    for anime_id in anime_ids:
        predicted_rating = svd_model.predict(user_id, anime_id).est  # Get the predicted rating
        predicted_ratings.append((anime_id, predicted_rating))
    
    # Sort the predictions by rating in descending order
    predicted_ratings.sort(key=lambda x: x[1], reverse=True)

    # Get the top 5 anime recommendations
    top_recommendations = predicted_ratings[:5]

    # Display the top 5 recommended anime
    top_animes = anime_df[anime_df['anime_id'].isin([x[0] for x in top_recommendations])]
    top_animes['predicted_rating'] = [x[1] for x in top_recommendations]

    st.write("Top 5 Recommendations based on Collaborative Filtering:")
    st.dataframe(top_animes[['name', 'genre', 'type', 'rating', 'predicted_rating']])

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "EDA", "Group Info", "Predictions"])

if page == "Home":
    st.write("Welcome to the Recommender System App!")
    set_video_background("Images/solo_leveling.png")

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
    set_video_background("Images/BG3.jpg")

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

    st.subheader("Top 10 Highest rated Anime")

     # Second graph: Top 10 Highest Rated Anime
    rating_v_anime = anime_exploded.groupby('name', as_index=False)['rating'].mean()
    top_10_anime = rating_v_anime.nlargest(10, 'rating')
    top_10_anime = top_10_anime.sort_values(by='rating', ascending=False)

    fig2 = px.bar(
        top_10_anime, 
        x='name', 
        y='rating', 
        color='name', 
        text=top_10_anime['rating'].round(1),
        title="Top 10 Highest Rated Anime",
        labels={'name': 'Anime Name', 'rating': 'Average Rating'},
        color_discrete_sequence=px.colors.sequential.Magma
    )

    fig2.update_traces(textposition='outside')
    fig2.update_layout(yaxis=dict(gridcolor='lightgray', griddash='dash'), width=1200, height=600)

    # Display the second graph in Streamlit
    st.plotly_chart(fig2, use_container_width=True)


elif page == "Group Info":
    set_video_background("Images/Pink.jpg")
    st.write("## Team Members")
    st.write("- Mpho Moloi : Trello and Streamlit")
    st.write("- Lebogang  Letsoalo : Slidedeck and Streamlit")
    st.write("- Thando Calana : Github Manager")
    st.write("- Thabang Maaphosa")
    st.write("- Thato Mzilikazi")
   

elif page == "Predictions":
    set_video_background("Images/Predic.png")
    anime_df = pd.read_csv("anime.csv")
    train_df = pd.read_csv("train.csv")

    def load_model(file_path):
        with gzip.open(file_path, 'rb') as f:
            model = pickle.load(f)
        return model

    svd_model = load_model("svd_model.pkl.gz")

    st.write("## Get Recommendations")
    st.write("Choose a recommendation model and input your preferences:")

    # Select recommendation model
    model_choice = st.selectbox("Choose Recommendation Model", ["Content-Based", "Collaborative Filtering"])

    # User input for preferred genre and type
    selected_genre = st.text_input("Preferred Genre (e.g., Action, Drama, Comedy)", "")

    if model_choice == "Content-Based" and selected_genre != "":
        content_based_recommendation(selected_genre, selected_type)

    elif model_choice == "Collaborative Filtering":
        # User ID input for collaborative filtering
        user_id = st.number_input("Enter your Anime ID", min_value=1, max_value=train_df['anime_id'].max(), step=1)

        # Make recommendations based on the SVD model
        collaborative_filtering(user_id, anime_df, svd_model)




