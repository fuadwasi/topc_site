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
                email_body= 'Dear '+ req_student.name + '\n\nYour registration for Take-Off Programming Contest Spring 2020 has been canceled sucessfully. \n'
                email_body+= 'Thanks for being with us\n\n With best regurds\nDIUCPC'
                email_subject = "TOPC Spring 2020 Registration cancellation"
                email_conf_send.email_send([registered_student.basic_info.email,registered_student.basic_info.sec_email],email_subject,email_body)
                messages.success(request,string)
                return redirect('ush')
            else:

                chk_queue= Req_queuey.objects.filter(token=req_student.token)
                if chk_queue:
                    string1 = "A request is alresdy pending for the id "+ req_student.sID+". Please wait till an admin approve it."
                    messages.success(request,string1)
                    return redirect('ush')

                else:
                    student_cancel_request = Req_queuey.objects.create(token=req_student.token,req_by=request.user.username,req_info=registered_student)
                    student_cancel_request.save()
                    string1 = "A request to cancel registration of Name: " +req_student.name+" ID: "+ req_student.sID + " has been sent to admin. Please wait till an admin approve it."
                    # email_conf_send(receiver_id,email_subject,email_body)
                    email_body = 'Dear ' + req_student.name + ',\n\nYour have requested us to cancel your registration for Take-Off Programming Contest Spring 2020.'
                    email_body += 'If you have not made requeat to cancel registration please contact in TOPC registration booth as soon as possible.\n\n'
                    email_body += 'Thanks for being with us\n\n With best regurds\nDIUCPC'
                    email_subject = "TOPC Spring 2020 Registration Cancellation Request Process"
                    email_conf_send.email_send([student_cancel_request.req_info.basic_info.email,student_cancel_request.req_info.basic_info.sec_email], email_subject,email_body)


                    messages.success(request, string1)
                    return  redirect('ush')

        else:
            string = "No registered student found."
            messages.error(request,string)

    else:

        messages.success(request,"You are not authenticated for this operation.")
        return redirect('home')

def request_list(request):
    if request.user.is_superuser:

        students = Req_queuey.objects.all()
        if request.method =="GET":
            context= {'user':request.user,'students':students}

        else:
            key = request.POST['search']
            students= Req_queuey.objects.filter(Q(token=key)|Q(req_info__sID__contains=key)|Q(req_info__basic_info__name__contains=key))
            context= {'user':request.user,'students':students}
        return render(request,'request_list.html',context)
    else:
        system_messages = messages.get_messages(request)
        for message in system_messages:
            # This iteration is necessary
            pass
        messages.error(request,"Access Denied")
        return redirect('ush')


def request_approve(request,id):
    token = id
    if request.user.is_superuser:
        chk_student = Req_queuey.objects.filter(token = token)
        if chk_student:
            req_student = ALLStudents.objects.get(token = token)
            registered_student = RegStudents.objects.get(token__exact=req_student.token)
            requested_std= Req_queuey.objects.get(token=token)
            req_student.status = "Not_Registered"
            string = "Registration of Token No: " + str(
                req_student.token) + " Name: " + req_student.name + " ID: " + str(req_student.sID) + " has been canceled"
            cancel_entry = Cancel_log.objects.create(
                token=req_student.token 	,
                sID		= req_student.sID 	  ,
                email	= req_student.email	  ,
                phone	= req_student.phone	  ,
                req_time= requested_std.req_time,
                req_by	= requested_std.req_by,
                cancel_by= request.user.username
            )
            cancel_entry.save()
            req_student.token = 99999
            registered_student.delete()
            req_student.save()
            # email_conf_send(receiver_id,email_subject,email_body)
            email_body= 'Dear  '+ req_student.name + '\n\nYour registration for Take-Off Programming Contest Spring 2020 has been canceled sucessfully. \n'
            email_body+= 'Thanks for being with us\n\n With best regards\nDIUCPC'
            email_subject = "TOPC Spring 2020 Registration Canceled"
            email_conf_send.email_send([req_student.email,req_student.sec_email], email_subject, email_body)
            messages.success(request,string)
            return redirect('request_list')
        else:
            messages.success(request,"No request found")
            return redirect('request_list')
    else:
        messages.success(request,"Not authorized")
        return redirect('ush')










def request_cancel(request,id):
    if request.user.is_superuser:
        chk_std= Req_queuey.objects.filter(Q(token__exact=id))
        if chk_std:
            req_student = Req_queuey.objects.get(token=id)
            name = req_student.req_info.basic_info.name
            string1 = "Registration cancellation request for Name: " + name + " ID: " + req_student.req_info.sID + " has been rejected."
            # email_conf_send(receiver_id,email_subject,email_body)

            email_body = 'Dear ' + name  + ',\n\nYour registration cancellation request for Take-Off Programming Contest Spring 2020.'
            email_body += 'has been rejected by DIUCPC. If you have any query about it Please come to the registration booth\n\n'
            email_body += 'Thanks for being with us\n\n With best regurds\nDIUCPC'
            email_subject = "TOPC Spring 2020 Registration Cancellation Request Rejected"
            email_conf_send.email_send([req_student.req_info.basic_info.email,req_student.req_info.basic_info.sec_email], email_subject, email_body)

            messages.success(request, string1)
            req_student.delete()
            return redirect('request_list')
        else:
            string1 ='No request found'
            messages.success(request, string1)
            return redirect('request_list')
    else:
        return  redirect('ush')