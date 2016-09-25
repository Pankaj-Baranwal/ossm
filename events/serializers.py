from rest_framework import serializers

from events.models import Team, Event


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        

class TeamSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        if self.validated_data['individual']:
            self.validated_data['second_member'] = None
            self.validated_data['nickname'] = '%s__%s' % (kwargs.get('owner').username, self.validated_data['event'].code)
            self.validated_data['name'] = '%s %s' % (kwargs.get('owner').get_full_name(), self.validated_data['event'].code)
        self.validated_data['first_member'] = kwargs.get('owner')
        kwargs.pop('owner')
        return super().save(**kwargs)

    class Meta:
        model = Team
        fields = ('nickname', 'name', 'event', 'first_member', 'second_member', 'individual')
