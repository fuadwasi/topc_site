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






def r_set(request, id):
    if request.user.is_staff:
        admin = User.objects.get(Q(id__exact=id))
        if request.user.is_staff:
            level = 2
        if request.user.is_superuser:
            level = 3

        if request.method == 'GET':
            context = {'admin': admin.username, 'level': level, 'user': request.user}

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
                            context = {'admin': admin.username, 'level': level, 'user': request.user,
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
                context = {'admin': admin.username, 'level': level, 'user': request.user,
                           'messages': "Wrong password entered"}
                return render(request, "reset_pass.html", context)

                context = {'students': all_user, 'level': level, 'user': request.user}
                messages.success(request, )
                return render(request, 'users.html', context)
    else:
        return redirect("ush")