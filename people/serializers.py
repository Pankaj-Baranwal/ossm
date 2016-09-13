from rest_framework import serializers

from people.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'contact', 'institute', 'city', 'state', 'verified')
