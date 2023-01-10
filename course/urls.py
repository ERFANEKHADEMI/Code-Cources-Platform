from django.urls import path 
from . import views

app_name='cources'

urlpatterns = [
    path('courses', views.catalog, name='catalog'),
    path('courses/<str:slug>', views.course, name='course'),
    
    path('create-course', views.createCourse, name='create-course'),
]
