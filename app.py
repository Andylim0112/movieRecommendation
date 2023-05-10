import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb
#streamlit run app.py
movie = Movie()
tmdb = TMDb()
tmdb.api_key = '1be696510002a8f9093b0258985e99c2'
tmdb.language = 'en-EN'


#using cos sim, return top ten movies that is most related according to given movie name
def get_recommendations(title):
    
    #get movie's index through movie name
    idx = movies[movies['title'] == title].index[0]
    
    #in cos sim metrix, get data according to given idx
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    #deescending order according to cos sim
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    #recommend ten movies except itself
    sim_scores = sim_scores[1:11]

    #indx of top ten recommended moveis
    movie_indices = [i[0] for i in sim_scores]

    #get movie name from indices
    images = []
    titles = []
    for i in movie_indices:
        id = movies['id'].iloc[i]
        details = movie.details(id)

        
        if details['poster_path']:
            images.append('https://image.tmdb.org/t/p/w500' + details['poster_path'])
        else:
            images.append('no_image.jpg')

        

        titles.append(details['title'])

    return images, titles




movies = pickle.load(open('movies.pickle', 'rb')) #, load pickled data.  read binary


cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

st.set_page_config(layout='wide')
st.header('Notflix')

movie_list = movies['title'].values
title = st.selectbox('Choose a movie you like', movie_list)
if st.button('Recommend'):
    with st.spinner('Please wait. . .'):
        images, titles = get_recommendations(title)

        idx = 0
        for i in range(0, 2):
            cols = st.columns(5)
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1