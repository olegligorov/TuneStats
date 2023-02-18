from django.urls import path
from .views import index, get_user_token, profile, auth_user, track, logout


urlpatterns = [
     path('get-auth-url', auth_user),
     path('', index),
     path('redirect', get_user_token),
     path('profile/logout/', logout),
     path('profile/<str:user>/', profile),
     path('<str:track_id>/', track)
]
