from django.urls import path
from .views import single_course , filter_data, course_details

urlpatterns = [
    path('', single_course, name='courses'),
    path('filter_data/', filter_data, name='filter_data'),
    path('details/<slug:slug>', course_details, name='course_details'),
]