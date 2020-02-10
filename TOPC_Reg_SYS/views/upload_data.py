from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect


def upload_data(request):
    if request.method == 'GET':
        if request.user.is_superuser:
            return render(request, 'upload-data.html', {"user": request.user})
        else:
            return redirect('ush')
    elif request.method == 'POST':
        filename = request.FILES['datafile']
        print('----------------------', filename)
        return HttpResponse('file uploaded')


def add_student(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'GET':
            return render(request, 'add-student.html', {"user": request.user})
        elif request.method == 'POST':
            return HttpResponse("user is added")
    else:
        return redirect('ush')
