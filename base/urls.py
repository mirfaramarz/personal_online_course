from django.urls import path
from .views import base, about_us, contact_us

urlpatterns = [
    path('', base, name='base'),
    path('about_us/', about_us, name='about_us'),
    path('contact_us/', contact_us, name='contact_us'),
]