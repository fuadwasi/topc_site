from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect

from TOPC_Reg_SYS.models import ALLStudents, Req_queuey

request_count = Req_queuey.objects.all().count()


# ,'request_count':request_count


def all_std(request):
    if request.user.is_staff:
        if request.method == 'GET':
            students = ALLStudents.objects.all()
            context = {'students': students, 'user': request.user, 'request_count': request_count}
            return render(request, 'all_std.html', context)
        elif request.method == "POST":
            key = request.POST['search']

            if key:
                get_std = ALLStudents.objects.filter(Q(sID__contains=key) | Q(name__contains=key))
                if get_std:
                    context = {'students': get_std, 'user': request.user, 'request_count': request_count}
                    return render(request, 'all_std.html', context)
                else:
                    messages.error(request, "No Student Data Found")
            else:
                messages.success(request, "Enter a valid user name or ID")
                return redirect('all_std')
    else:
        return redirect('usf')
