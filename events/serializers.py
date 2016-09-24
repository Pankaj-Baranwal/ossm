from rest_framework import serializers

from events.models import Team, Event


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('nickname', 'name', 'event', 'first_member', 'second_member')
