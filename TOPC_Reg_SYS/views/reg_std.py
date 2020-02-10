from django.contrib.auth.models import User
from django.shortcuts import render
import csv, io
from django.contrib import messages
from django.contrib.auth import authenticate, login  as auth_login, logout
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

from django.utils import timezone
from datetime import datetime
from django.db.models.functions import Now

from TOPC_Reg_SYS.models import ALLStudents, RegStudents


def reg_std(request):
    if request.user.is_staff:
        if request.method == 'GET':
            students = RegStudents.objects.all()
            context = {'students': students, 'user': request.user}
            return render(request, 'registered_student_list.html', context)
        elif request.method == "POST":
            key = request.POST['search']

            if key:
                get_std = RegStudents.objects.filter(Q(sID__contains=key) | Q(name__contains=key))
                if get_std:
                    context = {'students': get_std, 'user': request.user}
                    return render(request, 'registered_student_list.html', context)
                else:
                    messages.error(request, "No Student Data Found")
            else:
                messages.success(request, "Enter a valid user name or ID")
                return redirect('reg_std')
    else:
        return redirect('usf')

def register(request,id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            students = ALLStudents.objects.filter(Q(id__exact=id))
            if students:
                get_std = ALLStudents.objects.get(id=id)
                context = {'student': get_std, 'user': request.user}
                return render(request, 'std-reg.html', context)
            else:
                messages.success(request,"No student Data Found")
        elif request.method == "POST":

            get_std = ALLStudents.objects.get(id=id)
            if get_std.status!="Not_Registered":
                string = "User already registered."
                messages.success(request, string)
                return redirect('ush')

            shift = request.POST['shift']
            sem = request.POST['sem']
            sec = request.POST['sec']


            T_shirt = request.POST['T_shirt']
            email = request.POST['email']
            phone = request.POST['phone']
            regtiem = datetime.now()
            regby = request.user.username
            status = "Registered"



            # get_std.name = u_name

            get_std.semester = sem
            get_std.section = sec

            get_std.shift = shift
            get_std.t_shirt = T_shirt
            get_std.email = email
            get_std.phone = phone
            get_std.regtiem = regtiem
            get_std.regby = regby
            get_std.status = status
            get_std.save()








            if request.user.is_staff:
                u_name = request.POST['u_name']
                dept = request.POST['dept']
                campus = request.POST['campus']

                get_std.name = u_name
                get_std.department = dept
                get_std.campus = campus
                get_std.save()

            new_reg = RegStudents.objects.create(
                name = get_std.name 	  ,
                sID		= get_std.sID 	  ,
                department	= get_std.department	  ,
                semester 	= get_std.semester 	  ,
                section= get_std.section	  ,
                campus 	= get_std.campus  ,
                shift	= get_std.shift	  ,
                t_shirt	= get_std.t_shirt ,
                email	= get_std.email	  ,
                phone	= get_std.phone	  ,
                regtiem	= get_std.regtiem ,
                regby	= get_std.regby	  ,
                reg_status	= get_std.status
            )
            new_reg.save()
            new_std=RegStudents.objects.latest('id')
            new_std.token=new_std.id+1000
            new_std.userid="diu_topc_spr20_"+ str(new_std.id+1000)
            new_std.save()
            string= "Registration of " + new_std.name + " successful.\n Details:\n Name: " + new_std.name + "\nStudent ID: "+ new_std.sID +"\nToken no: "+ str(new_std.token)
            messages.success(request,string)
            return redirect('ush')

    else:
        return redirect('usf')
