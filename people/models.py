from django.contrib.auth import models
from django.db import models as db_models

# Create your models here.

STATES = (
    ('DL', 'Delhi'),
    ('WB', 'West Bengal'),
    ('TN', 'Tamil Nadu'),
    ('MH', 'Maharashtra')
)


class User(models.AbstractUser):
    contact = db_models.IntegerField(null=True)
    institute = db_models.CharField(max_length=100, null=True)
    city = db_models.CharField(max_length=50, null=True)
    state = db_models.CharField(max_length=2, choices=STATES, null=True)
    verified = db_models.BooleanField(default=False)

    def is_registered_event(self, event_id):
        return self.teams.filter(event=event_id).exists()
