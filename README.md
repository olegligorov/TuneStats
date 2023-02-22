# TuneStats
#### Spotify stat analysis web app, analyses your most listened tracks, artists and genres with content based track recommendation system

## Requirements:
install the requirements(dependencies) with `pip install -r requirements.txt`

## Endpoints

- /tunestats - main index page, the user can login through his spotify account
- /tunestats/get-auth-url - the user is redirected to the spotify authorization page
- /tunestats/redirect - after getting the user auth token the user is redirected to his profile page
- /tunestats/profile/{username} - user main page where he can see his most listened tracks, artists, genres, listening history
- /tunestats/profile/logout
- /tunestats/{trackId} - track page where the user can see the audio features of a track and the closest tracks by feature similarity (content based recommendation) 

## Services
- ApiService
- ChartService
- RecommenderService
- SpotifyService
