from rest_framework import serializers
from api import models
from django.core import exceptions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            'email',
            'first_name',
            'last_name',
            'date_joined',
            'password',
            'is_owner'
        )
        read_only_fields = ('date_joined', 'is_owner')


class PostSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        try:
            super(PostSerializer, self).save(self, **kwargs)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(e.message)

    class Meta:
        model = models.Post
        fields = ('uuid', 'truck', 'start_time', 'end_time', 'latitude', 'longitude')
        read_only_fields = ('uuid',)


class TruckSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for public view
    """
    class Meta:
        model = models.Truck
        fields = ('uuid', 'owner', 'title', 'description')
        read_only_fields = ('uuid',)


class MyTruckSerializer(serializers.ModelSerializer):
    """
    For editing trucks, the owner field automatically gets populated
    """
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Truck
        fields = ('uuid', 'owner', 'title', 'description')
        read_only_fields = ('uuid',)