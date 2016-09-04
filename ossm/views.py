from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    return render(request, 'base.html', {
        'pageTitle': 'ossm Dashboard',
        'youAreUsingJade': True,
        'full_name': request.user.is_superuser
    })


def login_landing(request):
    return render(request, 'account/login.html')
