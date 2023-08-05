import pandas as pd
import numpy as np
import pickle

similarity = pickle.load('D:\\Movie Recomendation System\\artifacts\\similarity.pkl')
movies_data = pd.read_csv('D:\\Movie Recomendation System\\artifacts\\combined_movies.csv')

def recomend(movie):
    movie_id = movies[movies['title'] == movie].index
    similarity[movie_id[0]]
    recomendations = sorted(list(enumerate(similarity[movie_id][0])) , key = lambda x : x[1] , reverse=True)[1:6]
    recomended_movies = []
    for i in recomendations:
        recomended_movies.append(movies['title'][i[0]])
    return recomended_movies
