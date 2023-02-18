from django.db import models

class Track(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    artist_id = models.CharField(max_length=150)
    track_id = models.CharField(max_length=150)
    image = models.CharField(max_length=150)
    album_name = models.CharField(max_length=150)

class Artist(models.Model):
    artist_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    spotify_url = models.CharField(max_length=150, default='')
    genres = models.CharField(max_length=150, default='')
    image = models.CharField(max_length=150, default='')

    def get_genres(self):
        return self.genres.split(',')