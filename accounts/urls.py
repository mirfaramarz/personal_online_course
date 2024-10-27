from django.urls import path
from .views import login_view, register, logout_view, activate, profile

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
]