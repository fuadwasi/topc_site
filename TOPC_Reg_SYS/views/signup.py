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