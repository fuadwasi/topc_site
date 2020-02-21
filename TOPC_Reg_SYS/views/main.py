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
from django.conf import settings
from TOPC_Reg_SYS.models import ALLStudents, RegStudents, Req_queuey




# Create your views here.
def home(request):
    request_count = Req_queuey.objects.all().count()
    if request.user.is_authenticated:
        return redirect("ush")
    else:
        if request.method == "GET":
            return render(request, 'index.html')

        elif request.method == "POST":
            system_messages = messages.get_messages(request)
            for message in system_messages:
                # This iteration is necessary
                pass
            system_messages.used = True
            sID = request.POST['search']

            if sID == '%':
                # obj = ALLStudents.objects.all()
                # if obj:
                #     context = {'students': obj}
                #     return render(request, "home.html", context)
                # else:
                messages.success(request, "No Data Found")
                return redirect('home')
            elif sID != "":
                obj = ALLStudents.objects.filter(Q(sID__contains=sID) | Q(name__contains=sID))

                if obj:
                    context = {'students': obj}
                    return render(request, "index.html", context)
                else:
                    messages.success(request, "No Data Found")
                    return redirect('home')
            else:
                messages.success(request, "No Data Entered")
                return redirect('home')


def login(request):
    request_count = Req_queuey.objects.all().count()
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
        if username == "" or password == "":
            messages.error(request, "Username and Password can't be empty")
            return redirect("login")

        chk_user = User.objects.filter(Q(username__exact=username))

        if chk_user:
            get_user = User.objects.get(Q(username__exact=username))
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # messages.success(request, "Login Successful")
                if get_user.is_staff:
                    return redirect('dashboard')
                else:
                    return redirect("ush")
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
    request_count = Req_queuey.objects.all().count()
    if request.user.is_authenticated:
        level = 0
        stdcount = RegStudents.objects.all().count()
        total_count = ALLStudents.objects.all().count()
        # return HttpResponse(request_count)
        if request.user.is_superuser:
            level = 3
        elif request.user.is_staff:
            level = 2
        else:
            level = 1
        if request.method == "GET":

            context = {'level': level, 'stdcount': stdcount, "total_count": total_count, "seat_avail": settings.SEAT_COUNT - stdcount,
                       'user': request.user, 'request_count': request_count}
            return render(request, "user_home.html", context)
        elif request.method == "POST":
            sID = request.POST['search']
            if sID == '':
                messages.success(request, "No Data Entered")
                return redirect('ush')
            if sID == '%':
                obj = ALLStudents.objects.all()
                if obj:
                    context = {'level': level, 'stdcount': stdcount, "total_count": total_count,
                               "seat_avail": settings.SEAT_COUNT - stdcount, 'students': obj, 'user': request.user,
                               'request_count': request_count}
                    return render(request, "user_home.html", context)
                else:
                    messages.success(request, "No Data Found")
                    return redirect('ush')
            elif sID != "":
                std = ALLStudents.objects.filter(Q(sID__contains=sID) | Q(name__contains=sID))

                if std:
                    context = {'level': level, 'stdcount': stdcount, 'students': std, "total_count": total_count,
                               "seat_avail": settings.SEAT_COUNT - stdcount, 'user': request.user, 'request_count': request_count}
                    return render(request, "user_home.html", context)
                else:
                    messages.success(request, "No Data Found")
                    return redirect('ush')
            else:
                context = {'level': level, 'stdcount': stdcount, "total_count": total_count,
                           "seat_avail": settings.SEAT_COUNT - stdcount, 'user': request.user, 'request_count': request_count}
                return render(request, "user_home.html", context)
    else:
        system_messages = messages.get_messages(request)
        for message in system_messages:
            # This iteration is necessary
            pass
        system_messages.used = True
        messages.error(request, "Please Login First")
        return redirect("login")


def users(request):
    request_count = Req_queuey.objects.all().count()
    if request.user.is_staff:
        level = 0
        stdcount = RegStudents.objects.all().count()
        if request.method == "GET":
            if request.user.is_staff:
                level = 2
                all_user = User.objects.filter(Q(is_superuser__exact=0))
            if request.user.is_superuser:
                level = 3
                all_user = User.objects.all()
        elif request.method == "POST":
            username = request.POST['search']
            if request.user.is_staff:
                level = 2
                all_user = User.objects.filter(Q(is_superuser__exact=0) & Q(username=username))
            if request.user.is_superuser:
                level = 3
                all_user = User.objects.filter(Q(username=username))
        context = {'students': all_user, 'level': level, 'user': request.user, 'request_count': request_count}
        return render(request, 'users.html', context)
    else:
        return redirect("ush")


def delete_user(request, id):
    request_count = Req_queuey.objects.all().count()
    system_messages = messages.get_messages(request)
    for message in system_messages:
        # This iteration is necessary
        pass
    system_messages.used = True
    if request.user.is_staff:
        level = 0
        if User.objects.all().count() == 0:
            messages.error(request, "There is no user.")
            return redirect("users")
        if request.user.is_staff:
            level = 2
            find_user = User.objects.filter(Q(is_superuser__exact=0) & Q(id__exact=id))
        if request.user.is_superuser:
            level = 3
            find_user = User.objects.filter(Q(id__exact=id))

        if find_user:
            current_user = User.objects.get(Q(id__exact=id))
            if current_user.username == request.user.username:
                messages.error(request, "You can't delete your self")
            elif current_user.username=='fusi':
                messages.success(request, "You Can't Delete This User")
            else:
                find_user.delete()
                messages.success(request, "User Deleted Successfully")
        else:
            messages.success(request, "User not found")
        return redirect('users')
    else:
        messages.error(request, "You are not authorized")
        return redirect("ush")
