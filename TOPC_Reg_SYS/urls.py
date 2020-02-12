from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.login, name="login"),
    path('logout/', views.user_logout, name='logout'),
    path('ush/', views.ush, name="ush"),
    path('signup/', views.signup, name="signup"),
    path('std-reg/', views.std_reg, name="std-reg"),
    path('users/', views.users, name="users"),
    path('r_set/<int:id>', views.r_set, name='r_set'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('upload-data/', views.upload_data, name='upload'),
    path('add-student/', views.add_student, name='add-student'),
    path('all_std/', views.all_std, name='all_std'),
    path('reg_std/', views.reg_std, name='reg_std'),
    path('register/<int:id>', views.register, name='register'),
]
