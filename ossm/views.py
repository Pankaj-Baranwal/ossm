import json

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer

from people.models import Subscription


def home(request):
    return render(request, 'base.html', {
        'user': request.user
    })


def subscribe(request):
    if request.method == 'POST':
        # data = json.loads(request.body)
        if 'email' in request.POST and request.POST['email'] != '':
            if Subscription.objects.filter(email=request.POST['email']).exists():
                return HttpResponse('Already subscribed', status=202)
            subscription = Subscription()
            subscription.email = request.POST['email']
            subscription.save()
            return HttpResponse('Subscribed successfully', status=201)
        else:
            return HttpResponseBadRequest('Invalid E-Mail Id.')
    else:
        return HttpResponseNotAllowed('Not allowed.')


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
