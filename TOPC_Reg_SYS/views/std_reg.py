from django.shortcuts import render


def std_reg(request):
    return render(request, 'std-reg.html')
