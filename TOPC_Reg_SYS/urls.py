from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('logout/', views.user_logout, name='logout'),
    path('ush/', views.ush, name="ush"),
]
