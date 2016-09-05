from django.shortcuts import render


def home(request):
    return render(request, 'ossm_base.html', {
        'user': request.user
    })
