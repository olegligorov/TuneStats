from django.test import TestCase, SimpleTestCase

from django.urls import reverse, resolve

import json
import unittest
from unittest.mock import patch

# from .webentities.track import Track
from .webentities.detailed_track import DetailedTrack
from .services.spotify_service import SpotifyService
from .services.chart_service import ChartService

from .models import Artist, Track


class SpotipyStub:
    def __init__(self):
        pass

    def current_user_recently_played(self, limit=50):
        data = ""
        with open('gui/json_test_examples/recently_listened_tracks.json') as f:
            data = json.load(f)
        return data

    def current_user(self):
        data = ""
        with open('gui/json_test_examples/user_details.json') as f:
            data = json.load(f)
        return data

    def current_user_top_artists(self, limit=50, time_range=""):
        data = ""
        with open('gui/json_test_examples/user_top_artists.json') as f:
            data = json.load(f)
        return data

    def current_user_top_tracks(self, limit=50, time_range=""):
        data = ""
        with open('gui/json_test_examples/user_top_tracks.json') as f:
            data = json.load(f)
        return data


    def artist(self, artist_id):
        data = ""
        with open('gui/json_test_examples/artist.json') as f:
            data = json.load(f)
        return data

    def track(self, track_id):
        data = ""
        with open('gui/json_test_examples/track.json') as f:
            data = json.load(f)
        return data

    def audio_features(self, track_id):
        data = ""
        with open('gui/json_test_examples/track_audio_features.json') as f:
            data = json.load(f)
        return data


class TestSpotifyService(TestCase):

    def setUp(self):
        self.sp = SpotipyStub()
        self.spotify_service = SpotifyService(self.sp)

    def test_get_user_listening_history(self):
        listening_history = self.spotify_service.get_user_listening_history()

        track1 = Track(name='Congratulations (feat. Bilal)',
                       artist='Mac Miller',
                       artist_id='4LLpKhyESsyAXpc4laK94U',
                       track_id='1OubIZ0ARYCUq5kceYUQiO',
                       image='https://i.scdn.co/image/ab67616d00001e022e92f776279eaf45d14a33fd',
                       album_name='The Divine Feminine')
        track2 = Track(name='Weekend (feat. Miguel)',
                       artist='Mac Miller',
                       artist_id='4LLpKhyESsyAXpc4laK94U',
                       track_id='6GnhWMhgJb7uyiiPEiEkDA',
                       image='https://i.scdn.co/image/ab67616d00001e02ee0f38410382a255e4fb15f4',
                       album_name='GO:OD AM')
        
        actual_listening_history = [track1, track2]
        for i in range(0, len(actual_listening_history)):
            self.assertEqual(actual_listening_history[i].name, listening_history[i].name)
            self.assertEqual(actual_listening_history[i].artist, listening_history[i].artist)
            self.assertEqual(actual_listening_history[i].artist_id, listening_history[i].artist_id)
            self.assertEqual(actual_listening_history[i].track_id, listening_history[i].track_id)
            self.assertEqual(actual_listening_history[i].image, listening_history[i].image)
            self.assertEqual(actual_listening_history[i].album_name, listening_history[i].album_name)
        # self.assertListEqual(listening_history, actual_listening_history)


    def test_get_current_user_data(self):

        expected_user_data = self.spotify_service.get_current_user_data()
        actual_user_data = {'username': 'Ole Gligorov',
                            'spotify_url': 'https://open.spotify.com/user/9lbbtu1rgt6ng8wld6rxrts46',
                            'id': '9lbbtu1rgt6ng8wld6rxrts46',
                            'image': 'https://i.scdn.co/image/ab6775700000ee857dd9175a0b8848cab3ff4559'}
        self.assertEqual(expected_user_data, actual_user_data)


    def test_get_user_top_artists(self):

        expected_user_top_artists = self.spotify_service.get_user_top_artists("medium_term")
        artist1 = Artist(artist_id="0iEtIxbK0KxaSlF7G42ZOp", name="Metro Boomin", spotify_url="https://open.spotify.com/artist/0iEtIxbK0KxaSlF7G42ZOp", genres="rap", image="https://i.scdn.co/image/ab67616100005174df9a1555f53a20087b8c5a5c")
        artist2 = Artist(artist_id="6l3HvQ5sa6mXTsMTB19rO5", name="J. Cole", spotify_url="https://open.spotify.com/artist/6l3HvQ5sa6mXTsMTB19rO5", genres="conscious hip hop,hip hop,north carolina hip hop,rap", image="https://i.scdn.co/image/ab67616100005174add503b411a712e277895c8a")
        actual_user_top_artists = [artist1, artist2]
        self.assertListEqual(expected_user_top_artists, actual_user_top_artists)
        

    def test_get_user_top_tracks(self):

        expected_user_top_tracks = self.spotify_service.get_user_top_tracks("medium_term")
        track1 = Track(name="Dirty Money (feat. Stonebwoy)",
                       artist="Jesse Royal",
                       artist_id= "4aXUVIuNCDbLoRAYfuVDi1",
                       track_id= "4EaYtxELrW9TbFdhxuunt8",
                       image= "https://i.scdn.co/image/ab67616d00001e02fc8326ef5d75d6d7f84db3ab",
                       album_name= "Royal")
        track2 = Track(name="Love Lost",
                       artist="Mac Miller",
                       artist_id="4LLpKhyESsyAXpc4laK94U",
                       track_id="0N9C80kcgL0xXGduKnYKWi",
                       image="https://i.scdn.co/image/ab67616d00001e022e8e9d480a55d914e1c5ff3b",
                       album_name="I Love Life, Thank You")
        actual_user_top_tracks = [track1, track2]
        for i in range(0, len(actual_user_top_tracks)):
            self.assertEqual(actual_user_top_tracks[i].name, expected_user_top_tracks[i].name)
            self.assertEqual(actual_user_top_tracks[i].artist, expected_user_top_tracks[i].artist)
            self.assertEqual(actual_user_top_tracks[i].artist_id, expected_user_top_tracks[i].artist_id)
            self.assertEqual(actual_user_top_tracks[i].track_id, expected_user_top_tracks[i].track_id)
            self.assertEqual(actual_user_top_tracks[i].image, expected_user_top_tracks[i].image)
            self.assertEqual(actual_user_top_tracks[i].album_name, expected_user_top_tracks[i].album_name)
        # self.assertListEqual(expected_user_top_tracks, actual_user_top_tracks)


    def test_get_user_top_genres(self):

        top_artists_one_month = self.spotify_service.get_user_top_artists_one_month()
        top_artists_six_months = self.spotify_service.get_user_top_artists_six_months()
        top_artists_lifetime = self.spotify_service.get_user_top_artists_lifetime()

        top_tracks_one_month = self.spotify_service.get_user_top_tracks_one_month()
        top_tracks_six_months = self.spotify_service.get_user_top_tracks_six_months()
        top_tracks_lifetime = self.spotify_service.get_user_top_tracks_lifetime()

        listening_history = self.spotify_service.get_user_listening_history()
        expected_genres = self.spotify_service.get_user_top_genres(top_artists_one_month=top_artists_one_month, 
                                                              top_artists_six_months=top_artists_six_months,
                                                              top_artists_one_year=top_artists_lifetime,
                                                              top_tracks_one_month=top_tracks_one_month,
                                                              top_tracks_six_months=top_tracks_six_months,
                                                              top_tracks_one_year=top_tracks_lifetime,
                                                              listening_history=listening_history)
        
        actual_genres = ['rap', 'conscious hip hop', 'hip hop', 'north carolina hip hop', 'dance pop', 'miami hip hop', 'pop', 'pop rap']
        self.assertListEqual(sorted(actual_genres), sorted(expected_genres))


    def test_get_track_data(self):
        chart_service = ChartService()

        track_id = "6EJiVf7U0p1BBfs0qqeb1f"
        actual_track_data = self.spotify_service.get_track_data(track_id=track_id)

        name = 'Cut To The Feeling'
        artist = 'Carly Rae Jepsen'
        artist_id = '6sFIWsNpZYqfjUpaCgueju'
        track_id = '6EJiVf7U0p1BBfs0qqeb1f'
        image = 'https://i.scdn.co/image/ab67616d00001e027359994525d219f64872d3b1'
        album_name = 'Cut To The Feeling'
        audio_features = self.sp.audio_features(track_id=track_id)[0]
        radio_chart = chart_service.get_audio_features_radar_chart(audio_features=audio_features)
        
        expected_track_data = DetailedTrack(name=name, artist=artist, artist_id=artist_id, track_id=track_id, image=image, album_name=album_name, audio_features=audio_features, radio_chart=radio_chart)
        self.assertEqual(actual_track_data.name, expected_track_data.name)
        self.assertEqual(actual_track_data.artist, expected_track_data.artist)
        self.assertEqual(actual_track_data.artist_id, expected_track_data.artist_id)
        self.assertEqual(actual_track_data.track_id, expected_track_data.track_id)
        self.assertEqual(actual_track_data.image, expected_track_data.image)
        self.assertEqual(actual_track_data.album_name, expected_track_data.album_name)
        self.assertEqual(actual_track_data.audio_features, expected_track_data.audio_features)



if __name__ == '__main__':
    unittest.main()

