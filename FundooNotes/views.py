from django.shortcuts import render


def startup(request):
    return render(request, 'user_auth/startup.html')
