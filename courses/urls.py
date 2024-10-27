from django.urls import path
from .views import single_course

urlpatterns = [
    path('course_list/', single_course, name='course_list')
]