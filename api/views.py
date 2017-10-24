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


# ======================== User Views ========================
class MyTrucksViewSet(viewsets.ModelViewSet):
    """
        Views for creating, updating and deleting a user's trucks
    """
    serializer_class = MyTruckSerializer
    lookup_field = 'uuid'
    queryset = Truck.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Truck.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class MyPostViewSet(viewsets.ModelViewSet):
    """
    Read-only views for all posts
    """
    serializer_class = PostSerializer
    lookup_field = 'post_uuid'
    queryset = Post.objects.all()

    def get_queryset(self):
        user = self.request.user
        truck_uuid = self.kwargs['truck_uuid']
        truck = Truck.objects.get(uuid=truck_uuid)

        # Verify that the user has access to that truck
        if truck.owner == user:
            return Post.objects.filter(truck=truck)
        else:
            return None