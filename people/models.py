from django.contrib.auth import models
from django.db import models as db_models
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

# Create your models here.
from haikunator import Haikunator

STATES = (
    ('DL', 'Delhi'),
    ('WB', 'West Bengal'),
    ('TN', 'Tamil Nadu'),
    ('MH', 'Maharashtra')
)


class User(models.AbstractUser):
    email = db_models.EmailField('email address', blank=False, unique=True, null=False)
    contact = db_models.IntegerField(null=True)
    institute = db_models.CharField(max_length=100, null=True)
    city = db_models.CharField(max_length=50, null=True)
    state = db_models.CharField(max_length=2, choices=STATES, null=True)
    verified = db_models.BooleanField(default=False)

    def is_registered_event(self, event_id):
        return self.teams.filter(event=event_id).exists()

    def save(self, *args, **kwargs):
        if self.pk is None:
            haikunator = Haikunator()
            self.username = haikunator.haikunate(token_length=0, delimiter='')
            while User.objects.filter(username=self.username).exists():
                self.username = haikunator.haikunate(token_length=0, delimiter='')

        super().save(*args, **kwargs)


class Contestant(db_models.Model):
    user = db_models.OneToOneField(User, to_field='username', on_delete=db_models.CASCADE, primary_key=True)
    hackerrank = db_models.CharField(max_length=30, default=None, null=True)
    data_gist_url = db_models.URLField(max_length=100, default=None, null=True)


class Subscription(db_models.Model):
    email = db_models.EmailField(null=False, primary_key=True)

    def _get_is_member(self):
        return User.objects.filter(email=self.email).exists()
    is_member = property(_get_is_member)

    def __str__(self):
        return self.email


class EmailRead(db_models.Model):
    email = db_models.EmailField(null=False, primary_key=True)
    timestamp = db_models.IntegerField(null=False)
    
    def __str__(self):
        return self.email


@receiver(user_signed_up, dispatch_uid="ossm.user_signed_up")
def user_signed_up_(request, user, **kwargs):
    contestant = Contestant()
    contestant.user = user
    contestant.hackerrank = None
    contestant.data_gist_url = None
    contestant.save()
