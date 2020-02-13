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

from django.conf import settings
from django.core.mail import send_mail


import smtplib



# def email_send(receiver_id,email_subject,email_body):
#     sender_id= settings.EMAIL_HOST_USER
#     # receiver_id = ['something@email.com','anything@email.com']
#     # send_mail(email_subject,email_body,sender_id,receiver_id, fail_silently= False)
#     send_mail(email_subject,email_body,sender_id,receiver_id, fail_silently= False)
#     return False
#
def email_send(receiver_id,email_subject,email_body):

    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)
        msg =f'Subject: {email_subject}\n\n {email_body}'
        smtp.sendmail(settings.EMAIL_HOST_USER,receiver_id,msg)


