from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect


def upload_data(request):
    if request.method == 'GET':
        if request.user.is_superuser:
            user = User.objects.get(username=request.user.username)
            return render(request, 'upload-data.html', {"user": user})
        else:
            return redirect('ush')
    elif request.method == 'POST':
        filename = request.FILES['datafile']
        print('------------------', filename)
        return HttpResponse("file uploaded")


