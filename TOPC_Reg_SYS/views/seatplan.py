from django.contrib.auth.models import User
from django.shortcuts import render
import csv, io
from django.contrib import messages
from django.contrib.auth import authenticate, login  as auth_login, logout
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.crypto import get_random_string
import random
import json
import string

from django.utils import timezone
from datetime import datetime
from django.db.models.functions import Now

from TOPC_Reg_SYS.models import ALLStudents, RegStudents, Room_data
from django.core import serializers
from . import email_conf_send


# send_mail(email_subject,email_body,sender_id,receiver_id, fail_silently= False)


#  ......................  Showing the list of registered students ................
def gen_seat_plan(request):
    all_student_data =  RegStudents.objects.all()
    for std in all_student_data:
        all_student = RegStudents.pr_data(std)
        print(all_student)
    # return JsonResponse({'result': list(all_student_data)})
    i =0
    j=0
    rooms = Room_data.objects.all()
    # room_seat
    # for student in all_student_data:


    return HttpResponse("hi")
