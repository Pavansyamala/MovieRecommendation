import streamlit as st 
import pandas as pd
import numpy as np
from src.components.model_trainer import recomend

movies_data = pd.read_csv('D:\Movie Recomendation System\artifacts\combined_movies.csv')
movie_names = movies_data['title'].values
st.title('Movie Recommendation System')
selected_movie = st.selectbox('Select Movie' ,
             movie_names
            )

if st.button('Recommend') :
  if selected_movie is None :
    st.write('Please select any one of the movie from the following')
  similar_movies = recommend(selected_movie)
  for i in similar_movies:
    st.write(i)
else :
  st.write('Click on Recommend Option for getting Movie')
