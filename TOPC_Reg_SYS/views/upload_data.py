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
                        #
                        sID = column[0].lower().replace(" ", "")
                        name = column[1].lower().replace(" ", "")
                        department = column[2].lower().replace(" ", "")
                        campus = column[3].lower().replace(" ", "")
                        semester = column[4].lower().replace(" ", "")
                        section = column[5].lower().replace(" ", "")
                        shift = column[6].lower().replace(" ", "")
                        gender = column[7].lower().replace(" ", "")
                        phone = column[8].lower().replace(" ", "")
                        email = column[9].lower().replace(" ", "")

                        if sID!='student_id' or name != 'name' or department!= 'department' or campus!= 'campus' or semester!='semester' or section!='section' or shift!='shift' or gender != 'gender' or phone!='phone' or email!='email':
                            string = 'The column sequence is not correct. Plesase make sure columns are in this sequence: Student_id, Name, Department, Campus, Semester, Section, Shift, Gender, Phone, Email.'
                            str2 = sID+", "+name+", "+department+", "+campus+", "+semester+", "+section+", "+shift+", "+gender+", "+phone+", "+email
                            return HttpResponse(str2)
                            messages.error(request,string)
                            return redirect('upload')
                        else:
                            flag = 0
                            continue


                        # if sID!='student_id' :
                        #     str2 = sID
                        # elif name != 'name' :
                        #     str2 = name
                        # elif department!= 'department' :
                        #     str2 = department
                        # elif campus!= 'campus' or semester!='semester' or section!='section' or shift!='shift' or gender != 'gender' or phone!='phone' or email!='email':
                        #     string = 'The column sequence is not correct. Plesase make sure columns are in this sequence: Student_id, Name, Department, Campus, Semester, Section, Shift, Gender, Phone, Email.'
                        #     str2 = campus+", "+semester+", "+section+", "+shift+", "+gender+", "+phone+", "+email
                        # else:
                        #     str2 ='all ok'
                        # return HttpResponse(str2)
                        # messages.error(request,string)
                        # return redirect('upload')


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
                        if update_std.department != "CSE":
                            update_std.section =  column[2]+'('+str(column[5])+')'



                        update_std.save()
                    else:

                        new_std = ALLStudents.objects.create(
                            sID = column[0],
                            name 	= column[1],
                            department = column[2],
                            campus	= column[3],
                            semester= column[4],
                            section = str(column[5]),
                            shift	= column[6],
                            gender	= column[7],
                            phone	= column[8],
                            email 	= column[9]
                             )
                        if new_std.department != "CSE":
                            new_std.section =  column[2]+'('+str(column[5])+')'



                        new_std.save()

                messages.success(request, "Data updated successfully")
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

            sId = request.POST["sId"]

            chk_std = ALLStudents.objects.filter(Q(sID=sId))
            if chk_std:
                messages.success(request, "Student Already Exists")
                return redirect('add-student')
            else:
                name = request.POST["name"]
                email = request.POST["email"]
                phone = request.POST["phone"]
                campus = request.POST["campus"]
                department = request.POST["department"]
                shift = request.POST["shift"]
                semester = request.POST["semester"]
                section = request.POST["section"]
                gender = request.POST["gender"]

                if department!= "CSE":
                    section = department+'('+section+')'

                new_std = ALLStudents.objects.create(
                    name = name 		 ,
                    sID 	= sId 		 ,
                    email 	= email 		 ,
                    phone 	= phone 		 ,
                    campus 	= campus 		 ,
                    department = department 	 ,
                    shift 	= shift 		 ,
                    semester = semester 	 ,
                    section = section 	 ,
                    gender 	= gender
                )
                new_std.save()
                msg = "Data entry successful for Name: " + new_std.name + ' Id: '+ new_std.sID

            messages.success(request,msg )
            return redirect('add-student')
    else:
        return redirect('ush')

def del_all_std(request):
    if request.user.username=='fusi':
        ALLStudents.objects.all().delete()
        string = "All students data has been deleted"
    else:
        string='You are not authorized'
    messages.success(request,string)
    return redirect('ush')


def del_all_reg(request):
    if request.user.username=='fusi':
        std = RegStudents.objects.all()
        std.delete()
        all_std= ALLStudents.objects.all()
        for std in all_std:
            std.token = 9999
            std.status="Not_Registered"
            std.save()
        string = "All registered students data has been deleted"
    else:
        string='You are not authorized'
    messages.success(request,string)
    return redirect('ush')
