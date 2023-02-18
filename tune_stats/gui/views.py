from django.shortcuts import render, redirect
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTHORIZATION_BASE_URL
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response

import spotipy
from .services.apiservice import APIService
from .services.recommender_service import RecommenderService


def index(request):
    return render(request, 'tunestats.html')


def auth_user(request):
    scope = 'user-top-read user-read-recently-played user-read-private user-read-email'
    url = Request('GET', AUTHORIZATION_BASE_URL, params={
        'scope': scope,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID
    }).prepare().url

    return redirect(url)


def get_user_token(request, format=None):
    code = request.GET.get('code')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    # get the username of the current user
    sp = spotipy.Spotify(auth=access_token)
    user_data = sp.current_user()
    username = user_data['display_name']

    # store the token
    request.session['user_token'] = access_token
    # redirect to the user home page
    return redirect(f'/tunestats/profile/{username}')


def logout(request):
    # invalidate the session and redirect the user to the login page
    request.session['user_token'] = ''
    return redirect('/tunestats')


def profile(request, user):
    user_token = request.session['user_token']

    if user_token == '':
        return redirect('/tunestats')

    api_service = APIService(user_token)
    user_data = api_service.get_current_user_data()

    top_artists_one_month = api_service.get_user_top_artists_one_month()
    top_artists_six_months = api_service.get_user_top_artists_six_months()
    top_artists_lifetime = api_service.get_user_top_artists_lifetime()

    top_tracks_one_month = api_service.get_user_top_tracks_one_month()
    top_tracks_six_months = api_service.get_user_top_tracks_six_months()
    top_tracks_lifetime = api_service.get_user_top_tracks_lifetime()

    listening_history = api_service.get_user_listening_history()
    genres = api_service.get_genres(top_artists_one_month, top_artists_six_months, top_artists_lifetime,
                                    top_tracks_one_month, top_tracks_six_months, top_tracks_lifetime, listening_history)

    context = {
        'user_data': user_data,
        'top_artists_one_month': top_artists_one_month,
        'top_artists_six_months': top_artists_six_months,
        'top_artists_lifetime': top_artists_lifetime,
        'top_tracks_one_month': top_tracks_one_month,
        'top_tracks_six_months': top_tracks_six_months,
        'top_tracks_lifetime': top_tracks_lifetime,
        'genres': genres,
        'listening_history': listening_history
    }

    return render(request, 'profile.html', context)


def track(request, track_id):
    user_token = request.session['user_token']

    if user_token == '':
        return redirect('/tunestats')

    api_service = APIService(user_token)
    recommender_service = RecommenderService(api_service)

    track_data = api_service.get_track_data(track_id)
    user_data = api_service.get_current_user_data()
    recommended_songs_ids = recommender_service.recommend_songs({
                                                                'id': track_id})
    recommended_songs = []

    for song in recommended_songs_ids:
        song = api_service.get_track_data(song['id'])
        recommended_songs.append(song)

    context = {
        "user_data": user_data,
        "track_data": track_data,
        "recommended_songs": recommended_songs
    }

    return render(request, 'track.html', context)
