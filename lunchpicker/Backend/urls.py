from django.urls import path
from dj_rest_auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('health', views.healthCheck, name="health-check"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('register', views.registerUser, name="register"),
    path('restaurant/create', views.createRestaurant, name="create-restaurant"),
    path('restaurant/list', views.getRestaurants, name="get-restaurants"),
    path('restaurant/upload/menu', views.uploadMenu, name="upload-menu"),
    path('restaurant/menu/date', views.getMenu, name="get-menu-by-date"),
    path('restaurant/menu/vote', views.vote_for_menu, name="vote"),
    path('restaurant/lunch/result', views.getResults, name="get-results")
    
]