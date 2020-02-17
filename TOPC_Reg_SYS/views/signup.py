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

from . import email_conf_send









def signup(request):
    if request.user.is_staff:
        if request.user.is_staff:
            level = 2
        if request.user.is_superuser:
            level = 3

        if request.method == 'GET':
            return render(request, "signup.html", {'user': request.user, "level": level})
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
                return render(request, "signup.html", {'msg': 'Data missing', 'user': request.user})
            else:
                if level < 3 and u_level == 'superuser':
                    messages(request, "Your are not authorized to do this  operation")
                    return redirect('signup')
                old_user = User.objects.filter(Q(username__exact=username))
                if old_user:
                    return render(request, "signup.html",
                                  {'msg': 'User Already Exists', 'user': request.user})
                elif password2 != password:
                    return render(request, "signup.html",
                                  {'msg': 'Password does not match', 'user': request.user})
                else:

                    new_user = User.objects.create_user(username=username, password=password, first_name=f_name, last_name=sId, email=email)
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
                    email_body = 'Dear ' + new_user.first_name + ',\n\nYour account has been created successfully.'
                    email_body += 'Your account details:\n\n'
                    email_body += '\nName: ' + new_user.first_name
                    email_body += '\nUsername: ' + new_user.username
                    email_body += '\nPassword: ' + password
                    email_body += '\nAuthentication Level: ' + u_level
                    email_body += '\n\n\nThanks for being with us.\n\n\n With best regurds\nDIUCPC'

                    email_subject = "TOPC Spring 2020 Registration Confirmation"
                    email_conf_send.email_send([new_user.email], email_subject, email_body)

                    messages.error(request, "User Registration Succcessful")
                    return redirect('signup')
                    # return render(request, "signup.html", {'msg': 'Entry Succcessful', 'user': request.user.username})
    else:
        return redirect("ush")