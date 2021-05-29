from django.urls import path

from forecast import views

app_name = 'forecast'
urlpatterns = [
    path('fibonacci/', views.fabonacci,name="fibonacci"),
]