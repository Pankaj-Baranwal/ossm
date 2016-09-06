from django.db import models
from people import models as people_models
from django.core.validators import RegexValidator


EVENTS = (
    (0, 'OSC'),
    (1, 'Esoteric'),
    (2, 'Debug your ass'),
    (3, 'Robotics')
)
# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=20, null=False)
    min_team_size = models.IntegerField(null=False, default=0)
    max_team_size = models.IntegerField(null=False, default=2)
    description = models.TextField()
    prize_1 = models.IntegerField(null=False, default=0)
    prize_2 = models.IntegerField(null=False, default=0)
    prize_3 = models.IntegerField(null=False, default=0)
    max_teams = models.IntegerField(null=False, default=15)


class Team(models.Model):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    nickname = models.CharField(max_length=20, null=True, validators=[alphanumeric])
    name = models.CharField(max_length=30, null=False)
    event = models.ForeignKey(to=Event)
    members = models.ManyToManyField(to=people_models.User, related_name='teams')

