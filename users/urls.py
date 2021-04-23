from django.urls import path

from users import views

app_name = 'users'
urlpatterns = [
    path('profile/', views.profile,name='profile'),
    path('profile_change/', views.change_profile,name='change_profile'),
]