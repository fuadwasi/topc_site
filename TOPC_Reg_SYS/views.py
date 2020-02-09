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


# Create your views here.
def home(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request,'user_home.html')
        else:
            return render(request,'home.html')

def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("ush")
        else:
            return render(request, "login.html")
    elif request.method == "POST":


        system_messages = messages.get_messages(request)
        for message in system_messages:
            # This iteration is necessary
            pass
        system_messages.used = True


        username = request.POST["u_name"]
        password = request.POST["password"]
        if username=="" or password =="":

            messages.error(request, "Username and Password can't be empty")
            return redirect("login")

        get_user = User.objects.get(Q(username__exact=username))

        if get_user:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Login Failed")
                return redirect("login")
        else:
            messages.error(request, "Problem with Username and Password")
            return redirect("login")

def user_logout(request):
    # return HttpResponse("Kita hoise??")
    logout(request)
    return redirect("home")


def ush(request):

    if request.user.is_authenticated:
        level = 0
        stdcount = RegStudents.objects.all().count()
        if request.user.is_staff:
            level = 2
        elif request.user.is_superuser:
            level = 3
        else:
            level = 1
        if request.method == "GET":
            context = {'level':level,'stdcount':stdcount}
            return render(request, "user_home.html",context)
        elif request.method == "POST":
            sID = request.POST['search']
            if sID =='%':
                obj = ALLStudents.objects.all()
                context = {'level': level,'stdcount':stdcount,'ALLstudents':obj}
                return render(request, "user_home.html", context)
            elif sID!="":
                std = ALLStudents.objects.filter(Q(sID__contains=sID) | Q(name__contains=sID))

                if std:
                    context = {'level': level, 'stdcount': stdcount, 'ALLstudents': std}
                    return render(request, "user_home.html", context)
                else:
                    pass
            else:
                context = {'level': level, 'stdcount': stdcount}
                return render(request, "user_home.html", context)
    else:
        system_messages = messages.get_messages(request)
        for message in system_messages:
            # This iteration is necessary
            pass
        system_messages.used = True
        messages.error(request,"Please Login First")
        return redirect("login")


