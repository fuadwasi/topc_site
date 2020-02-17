from django.contrib.auth.models import User
from django.shortcuts import render
import csv, io
from django.contrib import messages
from django.contrib.auth import authenticate, login  as auth_login, logout
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.crypto import get_random_string
import random
import string

from django.utils import timezone
from datetime import datetime
from django.db.models.functions import Now

from TOPC_Reg_SYS.models import ALLStudents, RegStudents
from . import email_conf_send
from django.conf import settings


def dashboard(request):
    all_campus= RegStudents.objects.all()
    total_std_count = ALLStudents.objects.all().count()
    total_reg_count = RegStudents.objects.all().count()
    seat_available=settings.SEAT_COUNT-total_reg_count
    main_campus = len(RegStudents.objects.filter(basic_info__campus='MC'))
    uttara_campus = len(RegStudents.objects.filter(basic_info__campus='UC'))
    male = len(RegStudents.objects.filter(basic_info__gender__exact='Male'))
    female = len(RegStudents.objects.filter(basic_info__gender__exact='Female'))
    day=len(RegStudents.objects.filter(basic_info__shift__exact='Day'))
    evening = len(RegStudents.objects.filter(basic_info__shift__exact='Evening'))
    m_size =len(RegStudents.objects.filter(t_shirt__exact='M'))
    l_size = len(RegStudents.objects.filter(t_shirt__exact='L'))
    xl_size = len(RegStudents.objects.filter(t_shirt__exact='XL'))
    xxl_size = len(RegStudents.objects.filter(t_shirt__exact='XXL'))
    xxxl_size = len(RegStudents.objects.filter(t_shirt__exact='XXXL'))
    cse = len(RegStudents.objects.filter(basic_info__department__exact="CSE"))
    swe = len(RegStudents.objects.filter(basic_info__department__exact="SWE"))
    cis = len(RegStudents.objects.filter(basic_info__department__exact="CIS"))
    other_dept = total_reg_count - cse - cis - swe
    A_1st = len(RegStudents.objects.filter(Q(basic_info__section__exact="A")& Q(basic_info__campus__exact="MC")& Q(basic_info__semester__exact="1st")& Q(basic_info__shift__exact="Day")))







    contex ={'total_std_count':total_std_count,
             'total_reg_count':total_reg_count,
             'seat_available':seat_available,
             'main_campus':main_campus,'uttara_camp':uttara_campus,
             'male':male,'female':female,
             'day':day,'evening':evening,
             'm_size' : m_size	,
             'l_size' 	: l_size    ,
             'xl_size' 	: xl_size   ,
             'xxl_size' : xxl_size  ,
             'xxxl_size' : xxxl_size ,
             'cse': cse,
             'swe': swe,
             'cis': cis,
             'other_dept':other_dept,
             'A_1st':A_1st,


             }


    # return HttpResponse(str(len(main_camp)))
    return render(request, 'dashboard.html',contex)
