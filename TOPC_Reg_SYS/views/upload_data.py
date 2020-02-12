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


def upload_data(request):
    # if request.method == 'GET':
    #     if request.user.is_superuser:
    #         return render(request, 'upload-data.html', {"user": request.user})
    #     else:
    #         return redirect('ush')
    # elif request.method == 'POST':
    #     filename = request.FILES['datafile']
    #     print('----------------------', filename)
    #     return HttpResponse('file uploaded')

    if request.user.is_superuser:
        if request.method == 'GET':
            return render(request, "upload-data.html", {'user': request.user})
        elif request.method == "POST":
            if request.FILES:
                csv_file = request.FILES['datafile']
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, "The file format is not correct. Please upload a *****.csv file")
                    return redirect('upload')
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                # next(io_string)
                flag = 1
                for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                    if flag == 1:
                        sID = column[0].lower()
                        name = column[1].lower()
                        department = column[2].lower()
                        campus = column[3].lower()
                        semester = column[4].lower()
                        section = column[5].lower()
                        shift = column[6].lower()
                        gender = column[7].lower()
                        phone = column[8].lower()
                        email = column[9].lower()
                        if sID!='student_id' or name != 'name' or department!= 'department' or campus!= 'campus' or semester!='semester' or section!='section' or shift!='shift' or gender != 'gender' or phone!='phone' or email!='email':
                            string = 'The column sequence is not correct. Plesase make sure columns are in this sequence: Student_id, Name, Department, Campus, Semester, Section, Shift, Gender, Phone, Email.'
                            messages.error(request,string)
                            return redirect('upload')
                        else:
                            flag = 0


                    sID=column[0]
                    check_std = ALLStudents.objects.filter(Q(sID__contains=sID))
                    if check_std:
                        update_std= ALLStudents.objects.get(sID=sID)
                        update_std.department = column[2]
                        update_std.campus = column[3]
                        update_std.semester = column[4]
                        update_std.section = column[5]
                        update_std.shift = column[6]
                        update_std.gender = column[7]
                        update_std.phone = column[8]
                        update_std.email = column[9]
                        update_std.save()
                    else:

                        new_std = ALLStudents.objects.create(
                            sID = column[0],
                            name 	= column[1],
                            department = column[2],
                            campus	= column[3],
                            semestr= column[4],
                            section = column[5],
                            shift	= column[6],
                            gender	= column[7],
                            phone	= column[8],
                            email 	= column[9]
                             )
                        new_std.save()

                messages.error(request, "Data updated successfully")
            else:
                messages.error(request, "No File detected")
            return redirect('upload')
        return redirect('upload')
    else:
        return redirect("ush")


def add_student(request):
    if request.user.is_staff:
        if request.method == 'GET':
            return render(request, 'add-student.html', {"user": request.user})
        elif request.method == 'POST':
            return HttpResponse("user is added")
    else:
        return redirect('ush')
