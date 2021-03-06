"""Personal_stock_investment_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #主页urls
    path('',include('homepage.urls')),
    #账户urls
    path('accounts/',include('allauth.urls')),
    path('accounts/',include('users.urls')),
    #股票urls
    path('stock/',include('stock.urls')),
    #通知urls
    path('inbox/notifications/',include('notifications.urls',namespace='notifications')),
    #消息urls
    path('notifications/',include('my_notification.urls')),
    #报告urls
    path('report/',include('report.urls')),
    #预测urls
    path('forecast/',include('forecast.urls')),
]
