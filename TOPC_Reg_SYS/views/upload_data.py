from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect


def upload_data(request):
    if request.user.is_staff or request.user.is_superuser:
        user = User.objects.get(username=request.user.username)
        return render(request, 'upload-data.html', {"user": user})
    else:
        return redirect('ush')

