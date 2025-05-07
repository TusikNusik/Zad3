from django.shortcuts import render
from trasy.models import PointList, Point
from rest_framework import generics, permissions
# Create your views here.
from .serializer import PointListSerializer, PointSerializer
from rest_framework.authentication import TokenAuthentication

class PointListCreateView(generics.ListCreateAPIView):
    serializer_class = PointListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PointList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PointListDetailDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = PointListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PointList.objects.filter(user=self.request.user)


class PointListView(generics.ListAPIView):
    serializer_class = PointSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        route = PointList.objects.get(id=self.kwargs['route_id'], user=self.request.user)
        return route.points.all()

class PointCreateView(generics.CreateAPIView):
    serializer_class = PointSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        route = PointList.objects.get(id=self.kwargs['route_id'], user=self.request.user)
        point = serializer.save()
        route.points.add(point)

class PointDeleteView(generics.DestroyAPIView):
    serializer_class = PointSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        route = PointList.objects.get(id=self.kwargs['route_id'], user=self.request.user)
        return route.points.get(id=self.kwargs['point_id'])