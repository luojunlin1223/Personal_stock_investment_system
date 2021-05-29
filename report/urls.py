from django.urls import path

from report import views

app_name = 'report'
urlpatterns = [
    path('monthly/', views.monthly,name="monthly"),
    path('seasonal/', views.seasonal, name="seasonal"),
    path('yearly/', views.yearly, name="yearly"),
]