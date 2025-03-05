import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import gzip
import base64
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 

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

# Load your preprocessed data and necessary components
anime_content = pd.read_csv('anime.csv') 
anime_content['name'] = anime_content['name'].astype(str)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "EDA", "Project Overview", "Group Info", "Predictions"])

if page == "Home":
    set_video_background("Images/solo_leveling.jpeg")
    st.title("Welcome to the Recommender System App!")

elif page == "Project Overview":
    set_video_background("Images/BG3.jpg")
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
    set_video_background("Images/BG3.jpg")
    st.title("Exploratory Data Analysis")

    # Display the dataset (Optional)
    st.subheader("Dataset Preview")
    st.write(anime_content.head())

    # Display Descriptive Statistics
    st.subheader("Descriptive Statistics for Categorical Data")
    st.write(anime_content.describe(include='O'))

    # Genre vs Rating Analysis
    st.subheader("Top 10 Genres by Average Rating")

    # Exploding genres into individual rows (Assumes genre is a comma-separated string)
    anime_exploded = anime_content.copy()
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
    st.write("- Mpho Moloi (Trello and Streamlit)")
    st.write("- Lebogang Letsoalo (Slide Deck and Streamlit)")
    st.write("- Thando Calana (GitHub Manager)")
    st.write("- Thabang Maaphosa")
    st.write("- Thato Mzilikazi")

# Predictions page content
elif page == "Predictions":
    set_video_background("Images/Predic.png")
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

    query = st.text_input("Enter anime name or ID to get recommendations:")

    if query:
        try:
            query = int(query)  # Convert to integer if it's an anime ID
        except ValueError:
            pass  # Otherwise, it's a name

    if model_choice == "Content-Based":

        anime_content['tags'] = anime_content['genre'] + " " + anime_content['type']
        anime_content = anime_content.drop(columns=['members', 'episodes'])
        vectorizer = TfidfVectorizer(stop_words='english')
        tag_matrix = vectorizer.fit_transform(anime_content['tags'])
        tag_similarity = cosine_similarity(tag_matrix)

        # Function to get top N recommendations, considering genre if specified
        def get_top_n_recommendations(query=None, selected_genre=None, N=10):
            if query:
                if isinstance(query, int):
                    anime_idx = anime_content.index[anime_content['anime_id'] == query].tolist()
                else:
                    anime_idx = anime_content.index[anime_content['name'].str.contains(query, case=False, na=False)].tolist()
                
                if not anime_idx:
                    return "No anime found with the given query."
                
                anime_idx = anime_idx[0]  # Take first match if multiple
                input_anime = anime_content.loc[anime_idx, 'name']
                sim_scores = list(enumerate(tag_similarity[anime_idx]))
                sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
                sim_scores = [s for s in sim_scores if s[0] != anime_idx]  # Exclude input anime

                # Convert results to DataFrame
                recommended_anime = anime_content.iloc[[i[0] for i in sim_scores]][['name', 'genre', 'type']]

                # If genre is specified, filter recommendations to contain the genre
                if selected_genre:
                    recommended_anime = recommended_anime[recommended_anime['genre'].str.contains(selected_genre, case=False, na=False)]

                # Limit to top N results
                recommended_anime = recommended_anime.head(N)

                st.write(f"The top {N} recommended anime similar to '{input_anime}' filtered by '{selected_genre}' are:")
                st.write(recommended_anime)
    
        recommendations = get_top_n_recommendations(query, selected_genre=selected_genre, N=5)

    elif model_choice == "Collaborative Filtering":

        def collaborative_filtering(query, anime_df, svd_model, selected_genre=None, N=5):
            if isinstance(query, int):  # Query is an anime ID
                anime_id = query
                input_anime = anime_df.loc[anime_df['anime_id'] == anime_id, 'name'].iloc[0]
            else:  # Query is an anime name
                anime_match = anime_df[anime_df['name'].str.contains(query, case=False, na=False)]
                if anime_match.empty:
                    st.write("No anime found with the given name.")
                    return
                input_anime = anime_match.iloc[0]['name']
                anime_id = anime_match.iloc[0]['anime_id']  # Take the first match if there are many with the same name

            anime_ids = anime_df['anime_id'].unique()
            predicted_ratings = [(anime, svd_model.predict(anime_id, anime).est) for anime in anime_ids]

            # Sort by predicted rating in descending order
            predicted_ratings.sort(key=lambda x: x[1], reverse=True)

            # Convert to DataFrame and merge to keep relevant details
            recommended_df = pd.DataFrame(predicted_ratings, columns=['anime_id', 'predicted_rating'])
            recommended_df = recommended_df.merge(anime_df, on='anime_id', how='left')
            
            if selected_genre:
                # Filter for anime that *contain* the specified genre
                genre_filtered = recommended_df[recommended_df['genre'].str.contains(selected_genre, case=False, na=False)]
                
                if genre_filtered.empty:
                    st.write(f"No anime found containing the genre '{selected_genre}', showing general recommendations.")
                    recommended_df = recommended_df.head(N)  # Show general recommendations if no genre match
                else:
                    recommended_df = genre_filtered.head(N)  # Get top N recommendations that contain the genre
                    recommended_df['name'] = recommended_df['name'].astype(str)
                    st.write(f"Here's the top {N} anime based on {input_anime} filtered by {selected_genre}:")
                    st.dataframe(recommended_df[['name', 'genre', 'type', 'rating']])
                    return
            else:
                recommended_df = recommended_df.head(N)  # Just take the top N recommendations if no genre is selected

            if not recommended_df.empty:
                recommended_df = recommended_df.head(N)
                recommended_df = recommended_df.sort_values(by='rating', ascending=False)
                recommended_df['name'] = recommended_df['name'].astype(str)

                st.write(f"Here's the top {N} anime based on {input_anime}:")
                st.dataframe(recommended_df[['name', 'genre', 'type', 'rating']])
            else:
                st.write("No recommendations found.")

        if query or selected_genre:
            collaborative_filtering(query, anime_content, svd_model, selected_genre=selected_genre, N=5)




