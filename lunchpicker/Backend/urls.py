from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name="routes"),
    path('health/', views.healthCheck, name="healthcheck"),
    
]