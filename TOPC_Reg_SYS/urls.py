from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('logout/', views.user_logout, name='logout'),
    path('ush/', views.ush, name="ush"),
    path('signup/', views.signup, name="signup"),
    path('users/',views.users,name="users"),
    path('r_set/<int:id>', views.r_set,name='r_set'),


]
