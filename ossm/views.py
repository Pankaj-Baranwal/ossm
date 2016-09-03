from django.shortcuts import render


def dashboard(request):
    return render(request, 'base.jade', {
        'pageTitle': 'ossm Dashboard',
        'youAreUsingJade': True
    })
