from rest_framework import serializers
from api import models


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
    class Meta:
        model = models.Post
        fields = ('uuid', 'truck', 'start_time', 'end_time', 'latitude', 'longitude')
        read_only_fields = ('uuid',)


class TruckSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = models.Truck
        fields = ('uuid', 'owner', 'title', 'description', 'posts')
        read_only_fields = ('uuid',)