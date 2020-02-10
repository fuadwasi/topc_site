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

def all_std(request):
    if request.user.is_staff:
        if request.method=='GET':
            students = ALLStudents.objects.all()
            context = {'students':students,'user':request.user}
            return render(request, 'all_std.html',context)
        elif request.method=="POST":
            key = request.POST['search']


            if key:
                get_std= ALLStudents.objects.filter(Q(sID__contains=key)|Q(name__contains=key))
                if get_std:
                    context = {'students': get_std, 'user': request.user}
                    return render(request, 'all_std.html', context)
                else:
                    messages.error(request,"No Student Data Found")
            else:
                messages.success(request, "Enter a valid user name or ID")
                return redirect('all_std')
    else:
        return redirect('usf')
