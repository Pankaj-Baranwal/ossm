from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'user': request.user
    })


def home(request):
    return render(request, 'ossm_base.html', {
        'user': request.user
    })


@login_required
def profile(request):
    return render(request, 'profile.html', {
        'user': request.user
    })
