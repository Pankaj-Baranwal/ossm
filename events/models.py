from django.db import models
from django.core.validators import RegexValidator
from django.db.models import Q

from people.models import User

EVENTS = (
    (0, 'OSC'),
    (1, 'Esoteric'),
    (2, 'Debug your ass'),
    (3, 'Robotics')
)
# Create your models here.


class Event(models.Model):
    code = models.CharField(max_length=2, null=False, unique=True)
    name = models.CharField(max_length=20, null=False)
    min_team_size = models.IntegerField(null=False, default=0)
    max_team_size = models.IntegerField(null=False, default=2)
    description = models.TextField()
    prize_1 = models.IntegerField(null=False, default=0)
    prize_2 = models.IntegerField(null=False, default=0)
    prize_3 = models.IntegerField(null=False, default=0)
    max_teams = models.IntegerField(null=False, default=15)

    def set_registered(self, user: User):
        if user.is_authenticated:
            teams = Team.objects.filter(event=self.code).all()
            self.registered = teams.filter(first_member__username=user.username).exists() or\
                              teams.filter(second_member__username=user.username).exists()
        else:
            self.registered = False

    def set_team(self, user: User):
        if user.is_authenticated:
            teams = Team.objects.filter(event=self.code).all()
            self.team = teams.filter(Q(first_member=user.username) | Q(second_member=user.username)).first()
        else:
            self.team = None


class Team(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    nickname = models.CharField(max_length=20, null=False, validators=[alphanumeric], unique=True)
    name = models.CharField(max_length=30, null=False, default='default', unique=True)
    event = models.ForeignKey(to=Event, to_field='code', null=False, blank=False)
    individual = models.BooleanField(null=False, default=True)
    first_member = models.ForeignKey(to='people.User', to_field='username', null=False, related_name='team_first_member')
    second_member = models.ForeignKey(to='people.User', to_field='username', null=True, related_name='team_second_member')

