from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.views.generic.detail import DetailView
from rest_framework import viewsets, mixins

from events.models import Team, Event

from .models import User, Subscription, EmailRead
from .serializers import UserSerializer, SubscriptionSerializer


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'user': request.user
    })


class Profile(DetailView):
    model = User
    template_names = ['profile.html']



class SubscriptionApiView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API end-points that allows subscriptions to be viewed or edited.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = ()



class SelfApiView(viewsets.ModelViewSet):
    """
    API end-points that allows user to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
