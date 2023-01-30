"""R4C URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from orders.views import OrderCreationView
from robots.views import index_view, GetRobotsCountView, PostRobotsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/create_order/', OrderCreationView.as_view(), name='order'),
    path('', index_view, name='index'),
    path('api/get_robots_count/', GetRobotsCountView.as_view(), name='path'),
    path('api/create_robots/', PostRobotsView.as_view(), name='create_robot'),
]
