from rest_framework import serializers

from people.models import User, Subscription


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'contact', 'institute', 'city', 'state', 'verified')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('email', 'is_member')
