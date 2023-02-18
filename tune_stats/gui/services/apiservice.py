from .spotify_service import SpotifyService
import spotipy

class APIService:
    # def __init__(self, access_token):
    #     self.service = SpotifyService(access_token)
    
    def __init__(self, access_token):
        sp = spotipy.Spotify(auth=access_token)
        self.service = SpotifyService(sp)

    def get_user_listening_history(self):
        return self.service.get_user_listening_history()
        
    def get_current_user_data(self):
        return self.service.get_current_user_data()

    def get_user_top_artists_one_month(self):
        return self.service.get_user_top_artists_one_month()
        
    def get_user_top_artists_six_months(self):
        return self.service.get_user_top_artists_six_months()

    def get_user_top_artists_lifetime(self):
        return self.service.get_user_top_artists_lifetime()

    def get_user_top_tracks_one_month(self):
        return self.service.get_user_top_tracks_one_month()

    def get_user_top_tracks_six_months(self):
        return self.service.get_user_top_tracks_six_months()
        
    def get_user_top_tracks_lifetime(self):
        return self.service.get_user_top_tracks_lifetime()
    
    def get_genres(self,top_artists_one_month, top_artists_six_months, top_artists_one_year, 
                        top_tracks_one_month, top_tracks_six_months, top_tracks_one_year, listening_history):
        return self.service.get_user_top_genres(top_artists_one_month, top_artists_six_months, top_artists_one_year, 
                        top_tracks_one_month, top_tracks_six_months, top_tracks_one_year, listening_history)
    
    def get_track_data(self, track_id):
        return self.service.get_track_data(track_id)
        
        