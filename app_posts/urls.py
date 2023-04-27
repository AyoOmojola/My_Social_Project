from django.urls import path
from app_posts import views

app_name = 'app_posts'

urlpatterns = [
    path('',views.home,name='home'),
    path('liked/<pk>/',views.liked,name='liked'),
    path('unliked/<pk>/',views.unliked,name='unliked')
]