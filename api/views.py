# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import *
from api.serializers import *
from api.permissions import *

from django.shortcuts import render

# Create your views here.

GITHUB_URL = 'https://github.com/cchyung/trollow-backend'


@api_view(['GET'])
def root_view(request):
    return Response({
        'message': 'Hello World!',
        'github': GITHUB_URL
    })


# ======================== Public Views ========================
class TruckViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only views for trucks
    """
    serializer_class = TruckSerializer
    lookup_field = 'uuid'
    queryset = Truck.objects.all()


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only views for all posts
    """
    serializer_class = PostSerializer
    lookup_field = 'post_uuid'
    queryset = Post.objects.all()

    def get_queryset(self):
        truck_uuid = self.kwargs['truck_uuid']
        truck = Truck.objects.get(uuid=truck_uuid)
        return Post.objects.filter(truck=truck)


@api_view(['GET'])
def like_truck(request, truck_uuid):
    """
    Lets users like a specific, finds truck from url, gets user
    from request data
    """
    truck = Truck.objects.all().get(uuid=truck_uuid)
    user = request.user
    # Check if like for this user and truck already exists
    if LikedTruck.objects.filter(truck=truck, user=user).count() < 1:
        data = {'truck': truck, 'user': user}
        ts = TruckLikeSerializer()  # Initialize an instance of the serializer
        ts.create(data)  # Create like based on data
        return Response({
            'message': 'Success!',
            'liked_truck': truck.uuid
        })

    else:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                'error': 'TruckAlreadyLikedError',
                'message': 'Truck ' + truck.uuid.__str__() + ' has already been liked by user ' + user.uuid.__str__()
        })

@api_view(['GET'])
def unlike_truck(request, truck_uuid):
    """
    For unliking trucks
    """
    truck = Truck.objects.all().get(uuid=truck_uuid)
    user = request.user
    # Check if like for this user and truck already exists
    like = LikedTruck.objects.filter(truck=truck, user=user)
    if like is not None:
        like.delete

    else:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                'error': 'TruckLikeNotFound',
                'message': 'Cannot find like for given truck and user'
        })


class CreateRatingView(generics.ListCreateAPIView):
    serializer_class = TruckRatingSerializer
    queryset = TruckRating.objects.all()

    def get_queryset(self):
        truck_uuid = self.kwargs['truck_uuid']
        truck = Truck.objects.get(uuid=truck_uuid)
        return TruckRating.objects.filter(truck=truck)

    # Custom create method
    def create(self, request, *args, **kwargs):
        # Fill in extra information form context
        truck_uuid = self.kwargs['truck_uuid']
        truck = Truck.objects.get(uuid=truck_uuid)
        user = request.user

        # Check if user already exists yet
        if TruckRating.objects.filter(truck=truck, user=user).count() < 1:
            data = request.data.copy()
            data['truck'] = truck.uuid
            data['user'] = user.uuid

            # Get serializer and validate data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'error': 'ReviewAlreadyExistsError',
                    'message': 'Review for truck ' + truck.uuid.__str__() + ' by user ' + user.email + ' already exists'
                }
            )


class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TruckRatingSerializer
    queryset = TruckRating.objects.all()
    lookup_field = 'id'

    permission_classes = (IsOwnerRatings,)

    def get_queryset(self):
        truck_uuid = self.kwargs['truck_uuid']
        truck = Truck.objects.get(uuid=truck_uuid)
        return TruckRating.objects.filter(truck=truck)


class MenuViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MenuItemSerializer
    lookup_field = 'slug'
    queryset = MenuItem.objects.all()

    def get_queryset(self):
        truck_uuid = self.kwargs['truck_uuid']
        truck = Truck.objects.get(uuid=truck_uuid)
        return MenuItem.objects.filter(truck=truck)


# ======================== User Views ========================
# ======================== Owner Views ========================
class MyTrucksViewSet(viewsets.ModelViewSet):
    """
        Views for creating, updating and deleting a user's trucks
    """
    serializer_class = MyTruckSerializer
    lookup_field = 'uuid'
    queryset = Truck.objects.all()

    permission_classes = (IsOwnerTrucks,)

    def get_queryset(self):
        user = self.request.user
        return Truck.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MyPostViewSet(viewsets.ModelViewSet):
    """
        Read-only views for all posts
    """
    serializer_class = PostSerializer
    lookup_field = 'post_uuid'
    queryset = Post.objects.all()

    permission_classes = (IsOwnerTruckObjects,)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        truck_uuid = self.kwargs['truck_uuid']
        data['truck'] = truck_uuid
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        user = self.request.user
        truck_uuid = self.kwargs['truck_uuid']
        truck = Truck.objects.get(uuid=truck_uuid)

        # Verify that the user has access to that truck
        if truck.owner == user:
            return Post.objects.filter(truck=truck)
        else:
            return None


class MyMenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer
    lookup_field = 'slug'
    queryset = MenuItem.objects.all()

    permission_classes = (IsOwnerTruckObjects,)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        truck_uuid = self.kwargs['truck_uuid']
        data['truck'] = truck_uuid
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        truck_uuid = self.kwargs['truck_uuid']
        truck = Truck.objects.get(uuid=truck_uuid)
        return MenuItem.objects.filter(truck=truck)


# ======================== Customer Views ========================
class MyTruckLikes(generics.ListAPIView):
    """
    List of a user's liked trucks
    """
    serializer_class = TruckLikeSerializer

    def get_queryset(self):
        user = self.request.user
        return LikedTruck.objects.filter(user=user)
