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

from TOPC_Reg_SYS.models import ALLStudents, RegStudents, Cancel_log, Req_queuey
from . import email_conf_send

# send_mail(email_subject,email_body,sender_id,receiver_id, fail_silently= False)



def cancel_request(request,id):
    system_messages = messages.get_messages(request)
    for message in system_messages:
        # This iteration is necessary
        pass
    system_messages.used = True
    if request.user.is_authenticated:
        chk_student= ALLStudents.objects.filter(id=id)
        if chk_student:
            req_student= ALLStudents.objects.get(id=id)
            registered_student = RegStudents.objects.get(token__exact=req_student.token)
            if request.user.is_superuser:

                req_student.status= "Not_Registered"
                string = "Registration of Token No: " + str(req_student.token)+ " Name: "+ req_student.name+" has been canceled"
                cancel_entry = Cancel_log.objects.create(
                    token	= req_student.token 	  ,
                    sID			= req_student.sID 	  ,
                    email		= req_student.email	  ,
                    phone		= req_student.phone	  ,
                    req_time	= datetime.now(),
                    req_by		= request.user.username ,
                    cancel_by	= request.user.username
                )
                cancel_entry.save()
                req_student.token = 99999
                registered_student.delete()
                req_student.save()
                # email_conf_send(receiver_id,email_subject,email_body)
                email_body= 'Dear '+ req_student.name + '\n\n Your registration for Take-Off Programming Contest Spring 2020 has been canceled sucessfully. \n'
                email_body+= 'Thanks for being with us\n\n With best regurds\nDIUCPC'
                email_subject = "TOPC Spring 2020 Registration cancellation"
                email_conf_send.email_send(['fuad15-9400@diu.edu.bd','erfanul15-10777@diu.edu.bd'],email_subject,email_body)
                messages.success(request,string)
                return redirect('ush')
            else:
                chk_queue= Req_queuey.objects.filter(token=req_student.token)
                if chk_queue:
                    str = "A request is alresdy pending for the id "+ req_student.sID+". Please wait till an admin approve it."
                    messages.success(request,str)
                    return redirect('ush')
                else:
                    student_cancel_request = Req_queuey.objects.create(token=req_student.token,req_by=request.user.username,req_info=registered_student)
                    student_cancel_request.save()
                    str = "A request to cancel registration of Name: " +req_student.name+" ID: "+ req_student.sID + " has been sent to admin. Please wait till an admin approve it."
                    # email_conf_send(receiver_id,email_subject,email_body)
                    email_body = 'Dear ' + req_student.name + ',\n\n Your have requested us to cancel your registration for Take-Off Programming Contest Spring 2020.'
                    email_body += 'If you have not made requeat to cancel registration please contact in TOPC registration booth as soon as possible.\n\n'
                    email_body += 'Thanks for being with us\n\n With best regurds\nDIUCPC'
                    email_subject = "TOPC Spring 2020 Registration cancellation"
                    email_conf_send.email_send(['fuad15-9400@diu.edu.bd', 'erfanul15-10777@diu.edu.bd'], email_subject,
                                               email_body)


                    messages.success(request, str)
                    return  redirect('ush')

        else:
            string = "No registered student found."
            messages.error(request,string)

    else:

        messages.success(request,"You are not authenticated for this operation.")
        return redirect('home')