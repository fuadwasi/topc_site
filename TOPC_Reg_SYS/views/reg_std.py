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


# send_mail(email_subject,email_body,sender_id,receiver_id, fail_silently= False)


#  ......................  Showing the list of registered students ................
def reg_std(request):
    if request.user.is_superuser:
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
        return redirect('ush')


#  ......................  New Student registration ................

def register(request, id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            students = ALLStudents.objects.filter(Q(id__exact=id))
            if students:
                get_std = ALLStudents.objects.get(id=id)
                context = {'student': get_std, 'user': request.user}
                return render(request, 'std-reg.html', context)
            else:
                messages.success(request, "No student Data Found")
        elif request.method == "POST":
            system_messages = messages.get_messages(request)
            for message in system_messages:
                # This iteration is necessary
                pass
            system_messages.used = True

            get_std = ALLStudents.objects.get(id=id)

            # if get_std.status!="Not_Registered":
            #     string = "User already registered."
            #     messages.success(request, string)
            #     return redirect('ush')

            gender = request.POST['gender']
            section = request.POST['section']
            email2 = request.POST['email2']
            phone2 = request.POST['phone2']
            t_shirt = request.POST['t_shirt']
            regtiem = datetime.now()
            regby = request.user.username
            status = "Registered"

            # get_std.name = u_name

            get_std.gender = gender
            get_std.section = section
            get_std.sec_email = email2
            get_std.sec_phone = phone2
            get_std.save()

            if get_std.status == 'Registered':
                # up_sid = get_std.sID
                update_std = RegStudents.objects.get(sID=get_std.sID)
                update_std.t_shirt = t_shirt
                string = "Data of " + get_std.name + " has beed updated successfully. Token no is" + str(
                    update_std.token)
                update_std.save()
                messages.success(request, string)
                return redirect('ush')

            if request.user.is_staff:
                campus = request.POST['campus']
                semester = request.POST['semester']
                get_std.campus = campus
                get_std.semester = semester
                get_std.save()

            get_std.status = status
            get_std.save()
            if request.user.is_superuser:
                name = request.POST['u_name']
                department = request.POST['department']
                get_std.name = name
                if department != "def_dep":
                    get_std.department = department
                get_std.save()

            new_reg = RegStudents.objects.create(
                sID	= get_std.sID 	  ,
                t_shirt	= t_shirt ,
                regby	= regby	  ,
                basic_info = get_std
            )
            new_reg.save()
            # letters = string.ascii_uppercase
            # password ''.join(random.choice(letters) for i in range(stringLength))
            pass_gen =get_random_string(length=10, allowed_chars='QWERTYUIOPASDFGHJKLZXCVBNM123456789')
            new_reg.password = pass_gen
            new_reg.token = new_reg.id + 1000
            get_std.token = new_reg.token
            get_std.save()
            new_reg.userid = "diu.topc.spr20." + str(new_reg.id + 1000)
            new_reg.save()
            string = "Registration of " + new_reg.basic_info.name + " successful.\n Details:\n Name: " + new_reg.basic_info.name + "\nStudent ID: " + new_reg.basic_info.sID + "\nToken no: " + str(
                new_reg.token)

            email_body = 'Dear ' + get_std.name + ',\n\n Your registration has been successfull for Take-Off Programming Contest, Spring 2020.'
            email_body += 'Your registration details:\n\n'
            email_body += '\nName: ' + get_std.name
            email_body += '\nID: ' + get_std.sID
            email_body += '\nToken No: ' + str(get_std.token)
            email_body += '\nT-Shirt Size: ' + new_reg.t_shirt
            email_body += '\nRegistration on: ' + str(new_reg.regtiem)
            email_body += '\n\n\nIf you have any confusion please come to the registraion booth and let us know.'
            email_body += 'Thanks for being with us\n\n\n With best regurds\nDIUCPC'

            email_subject = "TOPC Spring 2020 Registration Confirmation"
            email_conf_send.email_send([get_std.email,get_std.sec_email], email_subject, email_body)

            messages.success(request, string)
            return redirect('ush')

    else:
        return redirect('ush')
