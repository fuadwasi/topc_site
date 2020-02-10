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
            return redirect("ush")
        else:
            return render(request, 'home.html')


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
        if username == "" or password == "":
            messages.error(request, "Username and Password can't be empty")
            return redirect("login")

        get_user = User.objects.get(Q(username__exact=username))

        if get_user:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
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
    if request.user.is_authenticated:
        level = 0
        stdcount = RegStudents.objects.all().count()

        if request.user.is_superuser:
            level = 3
        elif request.user.is_staff:
            level = 2
        else:
            level = 1
        if request.method == "GET":
            context = {'level': level, 'stdcount': stdcount, 'user': request.user.username}
            return render(request, "user_home.html", context)
        elif request.method == "POST":
            sID = request.POST['search']
            if sID == '%':
                obj = ALLStudents.objects.all()
                context = {'level': level, 'stdcount': stdcount, 'ALLstudents': obj, 'user': request.user.username}
                return render(request, "user_home.html", context)
            elif sID != "":
                std = ALLStudents.objects.filter(Q(sID__contains=sID) | Q(name__contains=sID))

                if std:
                    context = {'level': level, 'stdcount': stdcount, 'ALLstudents': std, 'user': request.user.username}
                    return render(request, "user_home.html", context)
                else:
                    pass
            else:
                context = {'level': level, 'stdcount': stdcount, 'user': request.user.username}
                return render(request, "user_home.html", context)
    else:
        system_messages = messages.get_messages(request)
        for message in system_messages:
            # This iteration is necessary
            pass
        system_messages.used = True
        messages.error(request, "Please Login First")
        return redirect("login")


def signup(request):
    if request.user.is_staff:
        if request.user.is_staff:
            level = 2
        if request.user.is_superuser:
            level = 3

        if request.method == 'GET':
            return render(request, "signup.html", {'user': request.user.username, "level": level})
        elif request.method == "POST":

            system_messages = messages.get_messages(request)
            for message in system_messages:
                # This iteration is necessary
                pass
            system_messages.used = True

            username = request.POST["username"]
            f_name = request.POST["f_name"]
            email = request.POST["email"]
            sId = request.POST["sId"]
            password = request.POST["password"]

            password2 = request.POST["confirm_password"]
            u_level = request.POST["u_level"]
            if username == '' or password == '':
                return render(request, "signup.html", {'msg': 'Data missing', 'user': request.user.username})
            else:
                if level < 3 and u_level == 'superuser':
                    messages(request, "Your are not authorized to do this  operation")
                    return redirect('signup')
                old_user = User.objects.filter(Q(username__exact=username))
                if old_user:
                    return render(request, "signup.html",
                                  {'msg': 'User Already Exists', 'user': request.user.username})
                elif password2 != password:
                    return render(request, "signup.html",
                                  {'msg': 'Password does not match', 'user': request.user.username})
                else:

                    new_user = User.objects.create_user(username=username, password=password, first_name=f_name,
                                                        last_name=sId, email=email)
                    if u_level == 'superuser':
                        new_user.is_superuser = 1
                        new_user.is_staff = 1
                    elif u_level == 'admin':
                        new_user.is_superuser = 0
                        new_user.is_staff = 1
                    else:
                        new_user.is_superuser = 0
                        new_user.is_staff = 0
                    new_user.save()
                    messages.error(request, "Entry Succcessful")
                    return redirect('signup')
                    # return render(request, "signup.html", {'msg': 'Entry Succcessful', 'user': request.user.username})
    else:
        return redirect("ush")


def users(request):
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
        context = {'students': all_user, 'level': level, 'user': request.user.username}
        return render(request, 'users.html', context)
    else:
        return redirect("ush")


def r_set(request, id):
    if request.user.is_staff:
        admin = User.objects.get(Q(id__exact=id))
        if request.user.is_staff:
            level = 2
        if request.user.is_superuser:
            level = 3

        if request.method == 'GET':
            context = {'admin': admin.username, 'level': level, 'user': request.user.username}

            return render(request, 'reset_pass.html', context)
        elif request.method == "POST":
            system_messages = messages.get_messages(request)
            for message in system_messages:
                # This iteration is necessary
                pass
            system_messages.used = True
            pass
            password = request.POST["password"]

            password2 = request.POST["confirm_password"]

            current_admin_password = request.POST["admin_password"]
            current_admin = request.user
            current_user = authenticate(request, username=current_admin.username, password=current_admin_password)
            if current_user is not None:
                if request.user.is_staff:
                    level = 0
                    if request.user.is_staff:
                        level = 2
                    if request.user.is_superuser:
                        level = 3
                    if admin.is_superuser <= current_admin.is_superuser:
                        if password != password2 or password == '':
                            context = {'admin': admin.username, 'level': level, 'user': request.user.username,
                                       'messages': "New password is not valid"}
                            return render(request, "reset_pass.html", context)
                        else:
                            admin.set_password(password)
                            admin.save()
                            messages.success(request, "Password Change Successfully")
                            return redirect('users')
                    else:
                        messages.error(request, 'You are not authorized')
                        return redirect('users')
            else:
                context = {'admin': admin.username, 'level': level, 'user': request.user.username,
                           'messages': "Wrong password entered"}
                return render(request, "reset_pass.html", context)

                context = {'students': all_user, 'level': level, 'user': request.user.username}
                messages.success(request, )
                return render(request, 'users.html', context)
    else:
        return redirect("ush")


def delete_user(request, id):
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
            else:
                find_user.delete()
                messages.success(request, "User Deleted Successfully")
        else:
            messages.success(request, "User not found")
        return redirect('users')
    else:
        messages.error(request, "You are not authorized")
        return redirect("ush")
