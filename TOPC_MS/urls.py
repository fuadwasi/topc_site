from django.contrib import admin
from django.urls import path, include
from TOPC_Reg_SYS import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('TOPC_Reg_SYS.urls'))
]
