from django.shortcuts import render


def get_homepage(request):
    return render(request, 'landing_main.html')
