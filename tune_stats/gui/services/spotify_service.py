import spotipy
# from ..webentities.track import Track
from ..webentities.artist import ArtistModel
from collections import Counter
from .chart_service import ChartService


from ..webentities.detailed_track import DetailedTrack
from ..models import Track, Artist

class SpotifyService:
    # def __init__(self, access_token):
    #     self.sp = spotipy.Spotify(auth=access_token)
    #     self.charts = ChartService()

    def __init__(self, sp):
        self.sp = sp
        self.charts = ChartService()

    def get_user_listening_history(self): 
        listening_history = self.sp.current_user_recently_played(limit=50)
        result = []

        for item in listening_history["items"]:            
            name = item["track"]["name"]
            artist = item["track"]["album"]["artists"][0]["name"]
            artist_id = item["track"]["album"]["artists"][0]["id"]
            track_id = item["track"]["id"]
            image = item["track"]["album"]["images"][1]["url"]
            album_name = item["track"]["album"]["name"]
            # track = Track(name, artist, artist_id, track_id, image, album_name)
            track = Track(name=name, artist=artist, artist_id=artist_id, track_id=track_id, image=image, album_name=album_name)
            result.append(track)
        
        return result

    def get_current_user_data(self):
        user_data = self.sp.current_user()
        user = {}
        user["username"] = user_data["display_name"]
        user["spotify_url"] = user_data["external_urls"]["spotify"]
        user["id"] = user_data["id"]
        user["image"] = user_data["images"][0]["url"]
        return user

    def get_user_top_artists(self, range):
        top_artists = self.sp.current_user_top_artists(limit=50, time_range=range)
        result = []

        for item in top_artists["items"]:
            name = item["name"]
            id = item["id"]
            spotify_url = item["external_urls"]["spotify"]
            genres = tuple(item["genres"])
            genre_str = ','.join(genres)
            image = item["images"][1]["url"]
            
            artist = Artist(artist_id=id, name=name, spotify_url=spotify_url, genres=genre_str, image=image)
            oldArtist = Artist.objects.filter(artist_id=id)
            if not oldArtist.exists():
                artist.save()
                
            result.append(artist)
        return result

    def get_user_top_artists_one_month(self):
        return self.get_user_top_artists("short_term")

    def get_user_top_artists_six_months(self):
        return self.get_user_top_artists("medium_term")

    def get_user_top_artists_lifetime(self):
        return self.get_user_top_artists("long_term")

    def get_user_top_tracks(self, range):
        top_tracks = self.sp.current_user_top_tracks(limit=50, time_range=range)
        result = []

        for item in top_tracks["items"]:
            name = item["name"]
            artist = item["album"]["artists"][0]["name"]
            artist_id = item["album"]["artists"][0]["id"]
            track_id = item["id"]
            image = item["album"]["images"][1]["url"]
            album_name = item["album"]["name"]
            # track = Track(name, artist, artist_id, track_id, image, album_name)
            track = Track(name=name, artist=artist, artist_id=artist_id, track_id=track_id, image=image, album_name=album_name)

            result.append(track)
        return result

    def get_user_top_tracks_one_month(self):
        return self.get_user_top_tracks("short_term")

    def get_user_top_tracks_six_months(self):
        return self.get_user_top_tracks("medium_term")

    def get_user_top_tracks_lifetime(self):
        return self.get_user_top_tracks("long_term")
    
    def get_user_top_genres(self, 
                            top_artists_one_month, top_artists_six_months, top_artists_one_year, 
                            top_tracks_one_month, top_tracks_six_months, top_tracks_one_year, listening_history):
        artists = set()

        # add the artists from top_artists
        for artist in top_artists_one_month:
            artists.add(artist)
        for artist in top_artists_six_months:
            artists.add(artist)
        for artist in top_artists_one_year:
            artists.add(artist)


        for track in top_tracks_one_month + top_tracks_six_months + top_tracks_one_year + listening_history:
            artist_id = track.artist_id

            artist = Artist.objects.filter(artist_id=artist_id)
            if artist.exists():
                artist = artist[0]
            else: 
                # get the artist data from spotipy
                item = self.sp.artist(artist_id=artist_id)
                name = item["name"]
                id = item["id"]
                spotify_url = item["external_urls"]["spotify"]
                genres = tuple(item["genres"])
                image = item["images"][1]["url"]
                genre_str = ','.join(genres)
                artist = Artist(artist_id=id, name=name, spotify_url=spotify_url, genres=genre_str, image=image)
                # add the artist to the database
                artist.save()
            
            artists.add(artist)
        
        # count the occurances of each genre
        counter = Counter()
        for artist in artists:
            for genre in artist.get_genres():
                counter[genre] += 1
        
        genres = sorted(counter, key=counter.get, reverse=True)
        return genres
    

    def get_track_data(self, track_id):
        track_data = None
        track = Track.objects.filter(track_id=track_id)
        if track.exists(): 
            track_data = track[0]
        else:
            track_data = self.sp.track(track_id=track_id)
            name = track_data["name"]
            artist = track_data["album"]["artists"][0]["name"]
            artist_id = track_data["album"]["artists"][0]["id"]
            image = track_data["album"]["images"][1]["url"]
            album_name = track_data["album"]["name"]
            track_data = Track(name=name, artist=artist, artist_id=artist_id, track_id=track_id, image=image, album_name=album_name)
            track_data.save()

        audio_features = self.sp.audio_features(track_id)[0]

        radio_chart = self.charts.get_audio_features_radar_chart(audio_features)
        

        detailedTrack = DetailedTrack(name=track_data.name, artist=track_data.artist, artist_id=track_data.artist_id,
                                track_id=track_data.track_id, image=track_data.image, album_name=track_data.album_name,
                                radio_chart=radio_chart, audio_features=audio_features)

        return detailedTrack
    
    