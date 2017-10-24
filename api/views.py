# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import *
from api.serializers import *

from django.shortcuts import render

# Create your views here.

GITHUB_URL = 'https://github.com/cchyung/trollow-backend'


@api_view(['GET'])
def root_view(request):
    return Response({
        'message': 'Hello World!',
        'github': GITHUB_URL
    })


class TruckViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only views for trucks
    """
    serializer_class = TruckSerializer
    lookup_field = 'uuid'
    queryset = Truck.objects.all()


class PostViewSet(viewsets.ModelViewSet):
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


# class MyTrucks(viewsets.ModelViewSet):
    """
        Views for creating, updating and deleting a user's trucks
    """


class UserSignUp(generics.CreateAPIView):
    """
        Signup view
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TruckSchedule(generics.ListAPIView):
    """
    Displays a truck's schedule in order based on start-time
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        truck_uuid = self.kwargs['truck_uuid']
        truck = Truck.objects.get(uuid=truck_uuid)
        return Post.objects.filter(truck=truck)


class TruckPostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail view for a truck's post
    """
    serializer_class = PostSerializer

    lookup_field = 'uuid'

    def get_queryset(self):
        truck_uuid = self.kwargs['truck_uuid']
        truck = Truck.objects.get(uuid=truck_uuid)
        return Post.objects.filter(truck=truck)


