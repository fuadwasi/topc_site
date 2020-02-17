from django.contrib.auth.models import User
from django.shortcuts import render
import csv, io
from django.contrib import messages
from django.contrib.auth import authenticate, login  as auth_login, logout
from django.db.models import Q
from django.http import  HttpResponseRedirect
from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from django.utils.crypto import get_random_string
import random
import string

from django.utils import timezone
from datetime import datetime
from django.db.models.functions import Now

from TOPC_Reg_SYS.models import ALLStudents, RegStudents
from . import email_conf_send

def reg_std_download(request):
    if request.user.is_superuser:
        students = RegStudents.objects.all()
        response = HttpResponse(content_type='text/csv')
        dt = datetime.now()

        response['Content-Disposition'] = 'attachment; filename="TOPC_Spring20_Reg_Student_List_{}.csv"'.format(dt)
        writer = csv.writer(response, delimiter=',')
        writer.writerow(
            ['Token NO', 'ID', 'Name', 'Semester', 'Section', 'Department', 'Campus', 'Phone', 'Secondary_Phone',
             'Email', 'Secondary_Email', 'Room No', 'Pc', 'T_shirt','User_info' 'Username', 'Password'])
        for obj in students:
            writer.writerow([obj.token, obj.sID, obj.basic_info.name, obj.basic_info.section,
                             obj.basic_info.semester, obj.basic_info.department, obj.basic_info.campus,
                             obj.basic_info.phone, obj.basic_info.sec_phone, obj.basic_info.email,
                             obj.basic_info.sec_email, obj.room, obj.pc_no, obj.t_shirt,
                             obj.sID+'_'+obj.basic_info.semester+'_'+obj.basic_info.section+'_'+obj.basic_info.campus,

                             obj.userid, obj.password])

        return response
    else:
        string = "Access Denied"
        messages.success(request,string)
        return redirect('ush')