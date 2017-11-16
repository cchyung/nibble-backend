from rest_framework import serializers
from api import models
from django.core import exceptions
from api import services


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
            super(PostSerializer, self).save()
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

    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = models.Truck
        fields = ('uuid', 'posts', 'owner', 'title', 'description', 'genre', 'email', 'phone')
        read_only_fields = ('uuid',)


class TruckLikeSerializer(serializers.ModelSerializer):
    """
    For TruckLikes
    """
    truck = TruckSerializer(read_only=True)
    location = serializers.SerializerMethodField()

    def get_location(self, obj):
        current_location = services.get_current_truck_location(obj.truck)
        return current_location

    class Meta:
        model = models.LikedTruck
        fields = ('truck', 'user', 'location')


class TruckRatingSerializer(serializers.ModelSerializer):
    """
    Serializer for truck ratings
    """

    class Meta:
        model = models.TruckRating
        fields = ('id', 'truck', 'user', 'rating')


class MenuItemSerializer(serializers.ModelSerializer):
    """
    Serializer for menu items
    """

    class Meta:
        model = models.MenuItem
        fields = ('slug', 'truck', 'name', 'price', 'description', 'details')


class MyTruckSerializer(serializers.ModelSerializer):
    """
    For editing trucks.  The owner field automatically gets populated based on the request user
    """
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Truck
        fields = ('uuid', 'owner', 'title', 'description')
        read_only_fields = ('uuid',)