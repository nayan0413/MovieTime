import streamlit as st
import pandas as pd
import pickle
import requests
import creds

def get_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id, creds.key))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[index]
    recommended_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended = []
    movies_posters = []
    for i in recommended_movies:
        recommended.append(movies_list.iloc[i[0]].title)
        # we need to fetch poster for each movie
        movies_posters.append(get_poster(movies_list.iloc[i[0]].movie_id))
    return recommended, movies_posters

movies_list = pickle.load(open('movies.pkl', 'rb'))

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('MovieTime')

selected_movie = st.selectbox(
    "Enter Movie Name:",
    movies_list['title'].values,
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0])
        st.text(names[0])
    with col2:
        st.image(posters[1])
        st.text(names[1])
    with col3:
        st.image(posters[2])
        st.text(names[2])
    with col4:
        st.image(posters[3])
        st.text(names[3])
    with col5:
        st.image(posters[4])
        st.text(names[4])

