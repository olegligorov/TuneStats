import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist

from .spotify_service import SpotifyService
from .apiservice import APIService

from django.templatetags.static import static

class RecommenderService:
    def __init__(self, spotifyService : APIService):
        self.spotifyService = spotifyService
        self.data = pd.read_csv("gui/static/data.csv")
        
        self.number_cols = ['valence', 'acousticness', 'danceability', 'energy',
    'instrumentalness', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo']

    def find_song(self, song_id):
        # returns a dataframe with data for a song given the id.
        song_data = {}
        results = self.spotifyService.get_track_data(song_id)

        audio_features = results.audio_features

        song_data['name'] = results.name
        song_data['id'] = song_id

        for key, value in audio_features.items():
            song_data[key] = value

        return pd.DataFrame(song_data, index=[0])

    
    def get_song_data(self, song):
        try:
            song_data = self.data[(self.data['id'] == song['id'])].iloc[0]
            print('Fetching song information from local dataset')
            return song_data
        
        except IndexError:
            print('Fetching song information from spotify dataset')
            return self.find_song(song['id'])


    def get_mean_vector(self, song):
        # generates the mean vector of a song
        song_vectors = []
        song_data = self.get_song_data(song)
        
        song_vector = song_data[self.number_cols].values
        song_vectors.append(song_vector)  
        
        song_matrix = np.array(list(song_vectors))
        return np.mean(song_matrix, axis=0) 
    

    def recommend_songs(self, song, n_songs=7):
        metadata_cols = ['id']
        
        song_center = self.get_mean_vector(song)
        scaler = StandardScaler()
        scaler.fit(self.data[self.number_cols])
        scaled_data = scaler.transform(self.data[self.number_cols])
        scaled_song_center = scaler.transform(song_center.reshape(1, -1))
        distances = cdist(scaled_song_center, scaled_data, 'cosine')
        index = list(np.argsort(distances)[:, :n_songs][0])
        
        rec_songs = self.data.iloc[index]
        rec_songs = rec_songs[~rec_songs['id'].isin([song['id']])]
        return rec_songs[metadata_cols].to_dict(orient='records')