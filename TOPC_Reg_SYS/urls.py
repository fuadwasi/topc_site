from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

                  # load home on main.py to load landing page
                  path('', views.home, name="home"),

                  #   on main.py to load dashboard
                  path('dashboard/', views.dashboard, name="dashboard"),

                  #   on main.py load login page
                  path('login/', views.login, name="login"),

                  # on main.py to do logout
                  path('logout/', views.user_logout, name='logout'),

                  # on main.py to load login homepage
                  path('ush/', views.ush, name="ush"),

                  # on signup.py to signup different level users
                  path('signup/', views.signup, name="signup"),

                  # Seat plan genetare
                  path('gen_seat_plan/', views.gen_seat_plan, name="gen_seat_plan"),

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

                  # on upload.py to cancel all registration
                  path('del_all_reg/', views.del_all_reg, name='del_all_reg'),
                  # on upload.py to delete the student database
                  path('del_all_std/', views.del_all_std, name='del_all_std'),

                  # on
                  path('reg_std_download/', views.reg_std_download, name='reg_std_download'),
                  path('reg_std_full_download/', views.reg_std_full_download, name='reg_std_full_download'),
                  # path('seatplan/', views.seatplan, name='seatplan'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
