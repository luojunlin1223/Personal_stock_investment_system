from django.urls import path
from my_notification import views


app_name = 'my_notification'
urlpatterns = [
    path('read/', views.read_notifications,name="read_notifications"),
    path('delete/', views.delete_notifications,name="delete_notifications"),
    path('sign/', views.sign_to_read,name="sign_notifications"),
]