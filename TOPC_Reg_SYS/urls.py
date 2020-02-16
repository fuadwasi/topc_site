from django.urls import path

from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.login, name="login"),
    path('logout/', views.user_logout, name='logout'),
    path('ush/', views.ush, name="ush"),
    path('signup/', views.signup, name="signup"),

    path('users/', views.users, name="users"),
    path('r_set/<int:id>', views.pass_reset, name='r_set'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('upload-data/', views.upload_data, name='upload'),
    path('add-student/', views.add_student, name='add-student'),
    path('all_std/', views.all_std, name='all_std'),
    path('reg_std/', views.reg_std, name='reg_std'),
    path('register/<int:id>', views.register, name='register'),
    path('request/<int:id>', views.cancel_request, name='do_request'),
    path('request_approve/<int:id>', views.request_approve, name='request_approve'),
    path('request_cancel/<int:id>', views.request_cancel, name='request_cancel'),
    path('request_list/', views.request_list, name='request_list'),
    path('rank_upload/', views.rank_upload, name='rank_upload'),
    path('reg_std_download/', views.reg_std_download, name='reg_std_download'),
    path('del_all_reg/', views.del_all_reg, name='del_all_reg'),
    path('del_all_std/', views.del_all_std, name='del_all_std'),
]
