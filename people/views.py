from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets, mixins

from people.forms import ProfileForm
from .models import User, Subscription
from .serializers import UserSerializer, SubscriptionSerializer


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'user': request.user
    })


class Profile(TemplateView):
    model = User
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form
        }

    def post(self, request, *args, **kwargs):
        self.user = User.objects.get(username=request.user.username)
        self.form = ProfileForm(request.POST, instance=self.user)
        if self.form.is_valid():
            self.form.save()
        self.form = ProfileForm(instance=self.user)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        self.user = User.objects.get(username=request.user.username)
        self.form = ProfileForm(instance=self.user)
        return super().get(request, *args, **kwargs)


class SubscriptionApiView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    API end-points that allows subscriptions to be viewed or edited.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = ()


class SelfApiView(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    API end-points that allows user to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
