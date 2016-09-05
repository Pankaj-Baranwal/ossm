from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'user': request.user
    })


@login_required
def profile(request):
    return render(request, 'profile.html', {
        'user': request.user
    })
