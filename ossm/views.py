import time

from django.core.validators import validate_email
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.generic.edit import FormView
from rest_framework.renderers import JSONRenderer

from people.models import Subscription, EmailRead
from .forms import TeamForm


def home(request):
    return render(request, 'base.html', {
        'user': request.user
    })


class ContactView(FormView):
    template_name = 'contact_us.html'
    form_class = TeamForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return self.render_to_response(self.get_context_data(form=form))


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


def email_read(request):
    email = request.GET['email']
    if email:
        email_read = EmailRead()
        email_read.email = email
        email_read.timestamp = int(time.time())
        email_read.save()
        validate_email(email)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=200)


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
