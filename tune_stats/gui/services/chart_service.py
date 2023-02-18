import plotly.express as px
import pandas as pd

class ChartService:
    def get_audio_features_radar_chart(self, audio_features):
        danceability = audio_features['danceability']
        energy = audio_features['energy']
        speechiness = audio_features['speechiness']
        acousticness = audio_features['acousticness']
        instrumentalness = audio_features['instrumentalness']
        liveness = audio_features['liveness']
        valence = audio_features['valence']
        
        r = [danceability, energy, speechiness, acousticness, instrumentalness, liveness, valence]
        theta = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
        df = pd.DataFrame(dict(r=r, theta=theta))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
        # width=500, height=500
        fig.update_layout({
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font_color': '#FFFFFF',
            'font_size': 16,
        })
        
        html = fig.to_html(full_html=False)
        return html